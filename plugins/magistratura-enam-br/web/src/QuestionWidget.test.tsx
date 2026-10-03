import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QuestionWidget } from "./QuestionWidget";
import type { Question } from "./contracts";

const ready: Question = { session_id: "qsn_1234567890abcdef", projection: "public", state: "ready", subject: "Processo Civil", topic: "Provas", prompt: "Assinale a alternativa correta.", alternatives: (["A","B","C","D","E"] as const).map((id) => ({ id, text: `Alternativa ${id}` })), source_status: "caution", caution_notice: "Fontes canônicas parcialmente disponíveis." };
const corrected: Question = { ...ready, projection: "corrected", state: "answered", selected_option: "B", correct_option: "C", result: "incorrect", correction: { correct_rationale: "A alternativa C observa o CPC.", distractor_analysis: [{option:"A",analysis:"Erro A"},{option:"B",analysis:"Erro B"},{option:"D",analysis:"Erro D"},{option:"E",analysis:"Erro E"}], exceptions: [], traps: [] } };

beforeEach(() => {
  window.openai = { callTool: vi.fn() };
  vi.spyOn(window.parent, "postMessage").mockImplementation(message => {
    if (message.method === "ui/initialize") queueMicrotask(() => {
      window.dispatchEvent(new MessageEvent("message", { source: window.parent, data: {
        jsonrpc: "2.0", id: message.id, error: { code: -32601, message: "Only OpenAI bridge" },
      } }));
    });
  });
});
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

async function hostMessage(data: unknown) {
  await act(async () => {
    window.dispatchEvent(new MessageEvent("message", { source: window, data }));
  });
}

async function connectHost(legacy = false, initialQuestion?: Question, capabilities: Record<string, unknown> = {}, hostContext: Record<string, unknown> = {}) {
  vi.stubGlobal("ResizeObserver", class { observe() {} disconnect() {} });
  if (!legacy) window.openai = undefined;
  const post = vi.spyOn(window.parent, "postMessage").mockImplementation(() => {});
  render(<QuestionWidget initialQuestion={initialQuestion} />);
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "ui/initialize" }), "*"));
  const initialize = post.mock.calls.find(([message]) => message.method === "ui/initialize")![0];
  await hostMessage({ jsonrpc: "2.0", id: initialize.id, result: {
    protocolVersion: "2026-01-26", hostInfo: { name: "test-host", version: "1.0" },
    hostCapabilities: { serverTools: {}, ...capabilities }, hostContext,
  } });
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "ui/notifications/initialized" }), "*"));
  return post;
}

test("mostra cautela e mantém gabarito ausente antes da tentativa", () => {
  render(<QuestionWidget initialQuestion={ready} />);
  expect(screen.getByRole("alert")).toHaveTextContent("Cuidado");
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
  expect(screen.getAllByRole("radio")).toHaveLength(5);
  expect(screen.getByRole("button", {name:"Responder"})).toBeDisabled();
});

test("seleciona por teclado, envia e focaliza correção", async () => {
  const callTool = vi.fn().mockResolvedValue({ structuredContent: corrected });
  window.openai = { callTool };
  render(<QuestionWidget initialQuestion={ready} />);
  const radio = screen.getByRole("radio", {name:/Alternativa B/});
  await waitFor(() => expect(radio).toBeEnabled());
  radio.focus(); await userEvent.keyboard(" ");
  await userEvent.click(screen.getByRole("button", {name:"Responder"}));
  expect(callTool).toHaveBeenCalledWith("responder_questao", {session_id:ready.session_id, alternativa:"B"});
  expect((await screen.findByText(/gabarito C/)).closest("section")).toHaveFocus();
});

test("apresenta erro sem inventar correção", async () => {
  window.openai = { callTool: vi.fn().mockRejectedValue(new Error("offline")) };
  render(<QuestionWidget initialQuestion={ready} />);
  await userEvent.click(screen.getByRole("radio", {name:/Alternativa A/}));
  await userEvent.click(screen.getByRole("button", {name:"Responder"}));
  expect(await screen.findByText(/Não foi possível/)).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("carrega a questão pelo formato de resultado do bridge MCP Apps", async () => {
  await connectHost();
  expect(screen.getByText("Carregando questão…")).toBeInTheDocument();

  await act(async () => {
    window.dispatchEvent(new MessageEvent("message", {
      source: window,
      data: {
        jsonrpc: "2.0",
        method: "ui/notifications/tool-result",
        params: { structuredContent: ready },
      },
    }));
  });

  expect(await screen.findByRole("button", { name: "Responder" })).toBeInTheDocument();
  expect(screen.getByText(ready.prompt)).toBeInTheDocument();
});

test("resultado malformado encerra carregamento sem revelar dados privados", async () => {
  await connectHost();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: {
    structuredContent: { session_id: ready.session_id, projection: "private", correct_option: "C" },
  } });
  expect(await screen.findByText(/Não foi possível carregar a questão/)).toBeInTheDocument();
  expect(screen.queryByText("Carregando questão…")).not.toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("cancelamento pelo host encerra carregamento sem chamar ferramenta", async () => {
  const post = await connectHost();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-cancelled", params: { reason: "Permissão recusada" } });
  expect(await screen.findByText(/Não foi possível carregar a questão/)).toBeInTheDocument();
  expect(screen.queryByText("Carregando questão…")).not.toBeInTheDocument();
  expect(post.mock.calls.some(([message]) => message.method === "tools/call")).toBe(false);
});

test("MCP Apps aguarda resposta correlacionada e trata retorno tools/call", async () => {
  const post = await connectHost();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  expect(screen.getByRole("button", { name: "Corrigindo…" })).toBeDisabled();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  expect(screen.getByRole("button", { name: "Corrigindo…" })).toBeDisabled();
  const request = post.mock.calls.find(([message]) => message.method === "tools/call")![0];
  await hostMessage({ jsonrpc: "2.0", id: request.id, result: { content: [], structuredContent: corrected } });
  expect(await screen.findByText(/gabarito C/)).toBeInTheDocument();
});

test("MCP Apps apresenta erro retornado pela ferramenta", async () => {
  const post = await connectHost();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  const request = post.mock.calls.find(([message]) => message.method === "tools/call")![0];
  await hostMessage({ jsonrpc: "2.0", id: request.id, result: { content: [], isError: true } });
  expect(await screen.findByText(/Não foi possível/)).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("mostra fontes exceções e armadilhas somente na correção", async () => {
  const sources = [{ source_id: "src_cpc", kind: "planalto", title: "Código de Processo Civil", url: "https://www.planalto.gov.br/", accessed_at: "2026-10-02T12:00:00Z", role: "regra", excerpt: "Trecho da fonte" }];
  const full = { ...corrected, sources, correction: { ...corrected.correction!, exceptions: ["Exceção comprovada"], traps: ["Armadilha relevante"] } };
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: full }) };
  render(<QuestionWidget initialQuestion={{ ...ready, sources } as Question} />);
  expect(screen.queryByText("Código de Processo Civil")).not.toBeInTheDocument();
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  expect(await screen.findByRole("link", { name: "Código de Processo Civil" })).toHaveAttribute("href", "https://www.planalto.gov.br/");
  expect(screen.getByText("Exceção comprovada")).toBeInTheDocument();
  expect(screen.getByText("Armadilha relevante")).toBeInTheDocument();
  expect(screen.getByText("Trecho da fonte")).toBeInTheDocument();
});

test("sessão invalidada bloqueia tentativa e não mostra gabarito", () => {
  render(<QuestionWidget initialQuestion={{ ...ready, state: "invalidated", invalidation_reason: "Questão ambígua" } as unknown as Question} />);
  expect(screen.getByText("Questão ambígua")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Responder" })).not.toBeInTheDocument();
  for (const radio of screen.getAllByRole("radio")) expect(radio).toBeDisabled();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("notificações atrasadas não reabrem sessão respondida ou invalidada", async () => {
  render(<QuestionWidget initialQuestion={corrected} />);
  const notify = async (toolOutput: Question) => act(async () => {
    window.dispatchEvent(new CustomEvent("openai:set_globals", { detail: { globals: { toolOutput } } }));
  });
  await notify(ready);
  expect(screen.getByText(/gabarito C/)).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Responder" })).not.toBeInTheDocument();
  await notify({ ...ready, state: "invalidated", invalidation_reason: "Questão anulada" });
  await notify(corrected);
  expect(screen.getByText("Questão anulada")).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test.each([
  { sources: [null] },
  { sources: [{ title: "Fonte sem data" }] },
  { correction: { ...corrected.correction!, exceptions: [{}] } },
  { correction: { ...corrected.correction!, traps: [{}] } },
  { correction: { ...corrected.correction!, distractor_analysis: [null] } },
])("rejeita correção malformada sem quebrar o card: %j", async (broken) => {
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: { ...corrected, ...broken } }) };
  render(<QuestionWidget initialQuestion={ready} />);
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  expect(await screen.findByText(/Não foi possível/)).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("payload inicial malformado recebe erro visível", () => {
  window.openai!.toolOutput = { ...corrected, sources: [null] } as unknown as Question;
  render(<QuestionWidget />);
  expect(screen.getByText(/Não foi possível carregar/)).toBeInTheDocument();
});

test("ambos os bridges usam SDK e aguardam resultado depois da entrada", async () => {
  const legacy = window.openai!.callTool!;
  const post = await connectHost(true);
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: ready.session_id } } });
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input-partial", params: { arguments: { ...corrected, projection: "private" } } });
  expect(screen.getByText("Carregando questão…")).toBeInTheDocument();
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  const request = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  await hostMessage({ jsonrpc: "2.0", id: request.id, result: { content: [], structuredContent: corrected } });
  expect(await screen.findByText(/gabarito C/)).toBeInTheDocument();
  expect(legacy).not.toHaveBeenCalled();
});

test("timeout de resposta efetivada consulta estado sem reenviar a mutação", async () => {
  const legacy = window.openai!.callTool!;
  const post = await connectHost(true, ready);
  vi.useFakeTimers();
  fireEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  fireEvent.click(screen.getByRole("button", { name: "Responder" }));
  await act(async () => { await vi.advanceTimersByTimeAsync(30001); });
  const calls = post.mock.calls.map(([m]) => m).filter(m => m.method === "tools/call");
  expect(calls.filter(m => m.params.name === "responder_questao")).toHaveLength(1);
  const reading = calls.find(m => m.params.name === "renderizar_questao");
  expect(reading).toBeDefined();
  expect(screen.getByRole("button", { name: "Responder" })).toBeDisabled();
  await hostMessage({ jsonrpc: "2.0", id: reading.id, result: { content: [], structuredContent: corrected } });
  expect(screen.getByText(/gabarito C/)).toBeInTheDocument();
  expect(legacy).not.toHaveBeenCalled();
});

test("resultado tardio da tentativa anterior não substitui uma sessão nova", async () => {
  const post = await connectHost(false, ready);
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  const answering = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  const next = { ...ready, session_id: "qsn_abcdef1234567890", prompt: "Questão da sessão nova." };
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: next } });
  await hostMessage({ jsonrpc: "2.0", id: answering.id, result: { content: [], structuredContent: corrected } });
  expect(screen.getByText(next.prompt)).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("sessão nova pode responder enquanto chamada antiga ainda está pendente", async () => {
  const post = await connectHost(false, ready);
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  const next = { ...ready, session_id: "qsn_abcdef1234567890", prompt: "Sessão nova ainda pode responder." };
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: next } });
  await userEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  await userEvent.click(screen.getByRole("button", { name: "Responder" }));
  const calls = post.mock.calls.map(([m]) => m).filter(m => m.method === "tools/call" && m.params.name === "responder_questao");
  expect(calls).toHaveLength(2);
  await hostMessage({ jsonrpc: "2.0", id: calls[0].id, result: { content: [], structuredContent: corrected } });
  expect(screen.getByRole("button", { name: "Corrigindo…" })).toBeDisabled();
  await hostMessage({ jsonrpc: "2.0", id: calls[1].id, result: { content: [], structuredContent: { ...corrected, session_id: next.session_id } } });
  expect(screen.getByText(/gabarito C/)).toBeInTheDocument();
});

test("snapshot ready após falha não habilita repetição nem oculta o aviso", async () => {
  const post = await connectHost(false, ready);
  vi.useFakeTimers();
  fireEvent.click(screen.getByRole("radio", { name: /Alternativa B/ }));
  fireEvent.click(screen.getByRole("button", { name: "Responder" }));
  await act(async () => { await vi.advanceTimersByTimeAsync(30001); });
  const reading = post.mock.calls.map(([m]) => m).find(m => m.method === "tools/call" && m.params.name === "renderizar_questao");
  await hostMessage({ jsonrpc: "2.0", id: reading.id, result: { content: [], structuredContent: ready } });
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  expect(screen.getByText(/Não foi possível confirmar/)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Responder" })).toBeDisabled();
});

test("ações de continuidade respeitam tentativa e resultado", async () => {
  const view = render(<QuestionWidget initialQuestion={ready} />);
  expect(screen.queryByRole("button", { name: "Explique meu erro" })).not.toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Aprofunde esta distinção" })).not.toBeInTheDocument();
  view.unmount();
  render(<QuestionWidget initialQuestion={corrected} />);
  expect(screen.getByRole("button", { name: "Explique meu erro" })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Aprofunde esta distinção" })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Outra questão sobre este ponto" })).toBeInTheDocument();
});

test("legado revalida sessão e envia mensagem uma vez sem nova tentativa", async () => {
  const callTool = vi.fn().mockResolvedValue({ structuredContent: corrected });
  const sendFollowUpMessage = vi.fn().mockResolvedValue(undefined);
  window.openai = { callTool, sendFollowUpMessage };
  render(<QuestionWidget initialQuestion={corrected} />);
  const button = screen.getByRole("button", { name: "Explique meu erro" });
  await waitFor(() => expect(button).toBeEnabled());
  fireEvent.click(button); fireEvent.click(button);
  await waitFor(() => expect(sendFollowUpMessage).toHaveBeenCalledTimes(1));
  expect(callTool.mock.calls).toEqual([["obter_questao", { session_id: ready.session_id }]]);
  expect(sendFollowUpMessage.mock.calls[0][0].prompt).toContain(ready.session_id);
  expect(screen.getByText(/Pedido enviado ao chat/)).toBeInTheDocument();
});

test("host sem mensagens mostra texto copiável vinculado à sessão", async () => {
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: corrected }) };
  render(<QuestionWidget initialQuestion={corrected} />);
  const button = screen.getByRole("button", { name: "Aprofunde esta distinção" });
  await waitFor(() => expect(button).toBeEnabled());
  await userEvent.click(button);
  expect((await screen.findByRole("textbox", { name: "Pedido para copiar no chat" }) as HTMLTextAreaElement).value).toContain(ready.session_id);
  expect(screen.queryByText(/Pedido enviado/)).not.toBeInTheDocument();
});

test("invalidação no servidor impede aprofundamento e deixa apenas nova questão", async () => {
  const sendFollowUpMessage = vi.fn();
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: { ...ready, state: "invalidated", invalidation_reason: "Ambiguidade confirmada" } }), sendFollowUpMessage };
  render(<QuestionWidget initialQuestion={corrected} />);
  const button = screen.getByRole("button", { name: "Explique meu erro" });
  await waitFor(() => expect(button).toBeEnabled());
  await userEvent.click(button);
  expect(await screen.findByText("Ambiguidade confirmada")).toBeInTheDocument();
  expect(sendFollowUpMessage).not.toHaveBeenCalled();
  expect(screen.queryByRole("button", { name: "Explique meu erro" })).not.toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Aprofunde esta distinção" })).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Outra questão sobre este ponto" })).toBeInTheDocument();
});

test("falha de mensagem permite nova tentativa explícita sem anunciar envio", async () => {
  const sendFollowUpMessage = vi.fn().mockRejectedValueOnce(new Error("Recusado")).mockResolvedValue(undefined);
  const callTool = vi.fn().mockResolvedValue({ structuredContent: corrected });
  window.openai = { callTool, sendFollowUpMessage };
  render(<QuestionWidget initialQuestion={corrected} />);
  const button = screen.getByRole("button", { name: "Explique meu erro" });
  await waitFor(() => expect(button).toBeEnabled());
  await userEvent.click(button);
  expect(await screen.findByText(/Não foi possível enviar o pedido/)).toBeInTheDocument();
  expect(screen.queryByText(/Pedido enviado/)).not.toBeInTheDocument();
  await userEvent.click(button);
  expect(await screen.findByText(/Pedido enviado ao chat/)).toBeInTheDocument();
  expect(sendFollowUpMessage).toHaveBeenCalledTimes(2);
  expect(callTool.mock.calls.every(([name]) => name === "obter_questao")).toBe(true);
});

test("consulta de continuidade não refocaliza a correção já lida", async () => {
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: { ...corrected } }), sendFollowUpMessage: vi.fn().mockResolvedValue(undefined) };
  render(<QuestionWidget initialQuestion={corrected} />);
  const button = screen.getByRole("button", { name: "Aprofunde esta distinção" });
  await waitFor(() => expect(button).toBeEnabled());
  await userEvent.click(button);
  expect(await screen.findByText(/Pedido enviado ao chat/)).toBeInTheDocument();
  expect(button).toHaveFocus();
});

test("falha de contexto SDK não bloqueia mensagem autossuficiente", async () => {
  const post = await connectHost(false, corrected, { message: {}, updateModelContext: {} });
  await userEvent.click(screen.getByRole("button", { name: "Aprofunde esta distinção" }));
  const query = post.mock.calls.map(([m]) => m).find(m => m.method === "tools/call")!;
  expect(query.params.name).toBe("obter_questao");
  await hostMessage({ jsonrpc: "2.0", id: query.id, result: { content: [], structuredContent: corrected } });
  const context = post.mock.calls.map(([m]) => m).find(m => m.method === "ui/update-model-context")!;
  await hostMessage({ jsonrpc: "2.0", id: context.id, error: { code: -32603, message: "Context failed" } });
  const message = post.mock.calls.map(([m]) => m).find(m => m.method === "ui/message")!;
  expect(message.params.content[0].text).toContain(ready.session_id);
  expect(message.params.content[0].text).toContain("deepen_distinction");
  await hostMessage({ jsonrpc: "2.0", id: message.id, result: {} });
  expect(screen.getByText(/Pedido enviado ao chat/)).toBeInTheDocument();
});

test("mudança de sessão durante contexto impede envio do pedido anterior", async () => {
  const post = await connectHost(false, corrected, { message: {}, updateModelContext: {} });
  await userEvent.click(screen.getByRole("button", { name: "Explique meu erro" }));
  const query = post.mock.calls.map(([m]) => m).find(m => m.method === "tools/call")!;
  await hostMessage({ jsonrpc: "2.0", id: query.id, result: { content: [], structuredContent: corrected } });
  const context = post.mock.calls.map(([m]) => m).find(m => m.method === "ui/update-model-context")!;
  const next = { ...ready, session_id: "qsn_abcdef1234567890", prompt: "Questão nova durante contexto." };
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: next } });
  await hostMessage({ jsonrpc: "2.0", id: context.id, result: {} });
  expect(post.mock.calls.some(([m]) => m.method === "ui/message")).toBe(false);
  expect(screen.getByText(next.prompt)).toBeInTheDocument();
  expect(screen.queryByText(/Pedido enviado|Não foi possível enviar/)).not.toBeInTheDocument();
});

test("entrada de nova sessão sem resultado ainda impede mensagem da sessão anterior", async () => {
  const post = await connectHost(false, corrected, { message: {}, updateModelContext: {} });
  await userEvent.click(screen.getByRole("button", { name: "Explique meu erro" }));
  const query = post.mock.calls.map(([m]) => m).find(m => m.method === "tools/call")!;
  await hostMessage({ jsonrpc: "2.0", id: query.id, result: { content: [], structuredContent: corrected } });
  const context = post.mock.calls.map(([m]) => m).find(m => m.method === "ui/update-model-context")!;
  await hostMessage({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: "qsn_abcdef1234567890" } } });
  await hostMessage({ jsonrpc: "2.0", id: context.id, result: {} });
  expect(post.mock.calls.some(([m]) => m.method === "ui/message")).toBe(false);
  expect(screen.getByText(/Não foi possível enviar o pedido/)).toBeInTheDocument();
});

test("duas instâncias mantêm pedidos vinculados às respectivas sessões", async () => {
  const next = { ...corrected, session_id: "qsn_abcdef1234567890", prompt: "Segundo card." };
  const callTool = vi.fn().mockImplementation((_name, args) => Promise.resolve({ structuredContent: args.session_id === corrected.session_id ? corrected : next }));
  const sendFollowUpMessage = vi.fn().mockResolvedValue(undefined);
  window.openai = { callTool, sendFollowUpMessage };
  render(<><QuestionWidget initialQuestion={corrected} /><QuestionWidget initialQuestion={next} /></>);
  const cards = screen.getAllByRole("main");
  for (const card of cards) {
    const button = within(card).getByRole("button", { name: "Outra questão sobre este ponto" });
    await waitFor(() => expect(button).toBeEnabled());
    await userEvent.click(button);
  }
  await waitFor(() => expect(sendFollowUpMessage).toHaveBeenCalledTimes(2));
  expect(sendFollowUpMessage.mock.calls[0][0].prompt).toContain(corrected.session_id);
  expect(sendFollowUpMessage.mock.calls[1][0].prompt).toContain(next.session_id);
});

test('restaura escolha antes de salvar e persiste somente snapshot visual', async () => {
  const setWidgetState = vi.fn();
  window.openai = { callTool: vi.fn().mockResolvedValue({ structuredContent: corrected }), widgetState: { schema_version: '1.0.0', session_id: ready.session_id, selected_option: 'A', expanded: { distractors: false, sources: false } }, setWidgetState };
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeEnabled());
  expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeChecked();
  expect(setWidgetState).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole('radio', { name: /Alternativa B/ }));
  expect(setWidgetState).toHaveBeenLastCalledWith({ schema_version: '1.0.0', session_id: ready.session_id, selected_option: 'B', expanded: { distractors: false, sources: false } });
  await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
  await screen.findByText(/gabarito C/);
  expect(setWidgetState.mock.calls.at(-1)![0]).not.toHaveProperty('selected_option');
  const details = screen.getByText('Análise das demais alternativas').closest('details')!;
  details.open = true;
  fireEvent(details, new Event('toggle'));
  expect(setWidgetState.mock.calls.at(-1)![0]).toEqual({ schema_version: '1.0.0', session_id: ready.session_id, expanded: { distractors: true, sources: false } });
  expect(JSON.stringify(setWidgetState.mock.calls)).not.toMatch(/gabarito|correct_option|correction|fullscreen/);
});

test.each([ready, corrected, { ...ready, state: 'invalidated', invalidation_reason: 'Fonte superada' } as Question])('fullscreen e retorno preservam sessão em $state sem ferramentas', async initialQuestion => {
  const callTool = vi.fn();
  const requestDisplayMode = vi.fn().mockImplementation(async ({ mode }) => ({ mode }));
  window.openai = { callTool, displayMode: 'inline', requestDisplayMode };
  render(<QuestionWidget initialQuestion={initialQuestion} />);
  const expand = await screen.findByRole('button', { name: 'Expandir para estudar' });
  await waitFor(() => expect(expand).toBeEnabled());
  if (initialQuestion.state === 'ready') await userEvent.click(screen.getByRole('radio', { name: /Alternativa B/ }));
  await userEvent.click(expand);
  await userEvent.click(await screen.findByRole('button', { name: 'Voltar ao chat' }));
  expect(requestDisplayMode.mock.calls).toEqual([[{ mode: 'fullscreen' }], [{ mode: 'inline' }]]);
  expect(callTool).not.toHaveBeenCalled();
  expect(screen.getByText(initialQuestion.prompt)).toBeInTheDocument();
  if (initialQuestion.state === 'ready') expect(screen.getByRole('radio', { name: /Alternativa B/ })).toBeChecked();
});

test('fullscreen recusado mantém modo real e apresenta erro acessível', async () => {
  window.openai = { callTool: vi.fn(), displayMode: 'inline', requestDisplayMode: vi.fn().mockRejectedValue(new Error('Recusado')) };
  render(<QuestionWidget initialQuestion={ready} />);
  await userEvent.click(await screen.findByRole('button', { name: 'Expandir para estudar' }));
  expect(await screen.findByText(/Não foi possível mudar a apresentação/)).toHaveAttribute('role', 'alert');
  expect(screen.getByRole('button', { name: 'Expandir para estudar' })).toBeEnabled();
});

test('host sem fullscreen não mostra controle', async () => {
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa B/ })).toBeEnabled());
  expect(screen.queryByRole('button', { name: /Expandir|Voltar ao chat/ })).not.toBeInTheDocument();
});


test('SDK recebe mudança externa de modo e mantém escolha sem tool RPC', async () => {
  const post = await connectHost(false, ready, {}, { displayMode: 'inline', availableDisplayModes: ['inline', 'fullscreen'] });
  const radio = screen.getByRole('radio', { name: /Alternativa D/ });
  await waitFor(() => expect(radio).toBeEnabled());
  await userEvent.click(radio);
  await hostMessage({ jsonrpc: '2.0', method: 'ui/notifications/host-context-changed', params: { displayMode: 'fullscreen' } });
  expect(screen.getByRole('button', { name: 'Voltar ao chat' })).toBeEnabled();
  expect(screen.getByRole('main')).toHaveAttribute('data-display-mode', 'fullscreen');
  expect(radio).toBeChecked();
  expect(post.mock.calls.some(([m]) => ['ui/request-display-mode', 'tools/call'].includes(m.method))).toBe(false);
});

test('pedido pendente de fullscreen bloqueia clique duplo; confirmação inline não simula expansão', async () => {
  let resolve!: (result: { mode: 'inline' }) => void;
  const requestDisplayMode = vi.fn().mockImplementation(() => new Promise(done => { resolve = done; }));
  window.openai = { callTool: vi.fn(), displayMode: 'inline', requestDisplayMode };
  render(<QuestionWidget initialQuestion={ready} />);
  const button = await screen.findByRole('button', { name: 'Expandir para estudar' });
  await waitFor(() => expect(button).toBeEnabled());
  fireEvent.click(button); fireEvent.click(button);
  expect(button).toBeDisabled();
  expect(requestDisplayMode).toHaveBeenCalledTimes(1);
  await act(async () => resolve({ mode: 'inline' }));
  expect(button).toBeEnabled();
  expect(screen.getByRole('main')).toHaveAttribute('data-display-mode', 'inline');
});

test('nova sessão e invalidação limpam estado visual e snapshots privados nunca são restaurados', async () => {
  const setWidgetState = vi.fn();
  window.openai = { callTool: vi.fn(), setWidgetState, widgetState: { schema_version: '1.0.0', session_id: ready.session_id, selected_option: 'B', expanded: { distractors: true, sources: true }, correct_option: 'C' } };
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa B/ })).toBeEnabled());
  expect(screen.getByRole('radio', { name: /Alternativa B/ })).not.toBeChecked();
  await userEvent.click(screen.getByRole('radio', { name: /Alternativa B/ }));
  const next = { ...ready, session_id: 'qsn_abcdef1234567890', prompt: 'Nova questão' };
  await act(async () => window.dispatchEvent(new CustomEvent('openai:set_globals', { detail: { globals: { toolInput: { session_id: next.session_id }, toolOutput: next } } })));
  expect(screen.getByRole('radio', { name: /Alternativa B/ })).not.toBeChecked();
  await userEvent.click(screen.getByRole('radio', { name: /Alternativa A/ }));
  await act(async () => window.dispatchEvent(new CustomEvent('openai:set_globals', { detail: { globals: { toolOutput: { ...next, state: 'invalidated', invalidation_reason: 'Fonte superada' } } } })));
  expect(setWidgetState.mock.calls.at(-1)![0]).toEqual({ schema_version: '1.0.0', session_id: next.session_id, expanded: { distractors: false, sources: false } });
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test('painéis da correção sobrevivem à expansão e retorno; seleção vem do servidor', async () => {
  const requestDisplayMode = vi.fn().mockImplementation(async ({ mode }) => ({ mode }));
  const sources = [{ source_id: 'src_1', kind: 'official', title: 'Fonte extensa', accessed_at: '2026-10-03', role: 'correction', excerpt: 'Trecho longo' }];
  window.openai = { callTool: vi.fn(), requestDisplayMode, displayMode: 'inline', widgetState: { schema_version: '1.0.0', session_id: ready.session_id, selected_option: 'A', expanded: { distractors: true, sources: true } } };
  render(<QuestionWidget initialQuestion={{ ...corrected, sources }} />);
  expect(screen.getByRole('radio', { name: /Alternativa B/ })).toBeChecked();
  expect(screen.getByText('Fontes da correção').closest('details')).toHaveAttribute('open');
  await userEvent.click(await screen.findByRole('button', { name: 'Expandir para estudar' }));
  await userEvent.click(await screen.findByRole('button', { name: 'Voltar ao chat' }));
  expect(screen.getByText('Análise das demais alternativas').closest('details')).toHaveAttribute('open');
  expect(screen.getByText('Fontes da correção').closest('details')).toHaveAttribute('open');
  expect(screen.getByText('Trecho longo')).toBeInTheDocument();
});

test('modos anunciados no bridge sem método de apresentação não oferecem controle', async () => {
  window.openai = { callTool: vi.fn(), availableDisplayModes: ['inline', 'fullscreen'], displayMode: 'inline' };
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeEnabled());
  expect(screen.queryByRole('button', { name: 'Expandir para estudar' })).not.toBeInTheDocument();
});

test('API de armazenamento indisponível não impede estudar', async () => {
  window.openai = { callTool: vi.fn(), get widgetState() { throw new Error('Indisponível'); }, setWidgetState: () => { throw new Error('Indisponível'); } };
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeEnabled());
  await userEvent.click(screen.getByRole('radio', { name: /Alternativa A/ }));
  expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeChecked();
});

test('notificação externa legado muda controle sem pedido; tema não desfaz modos negociados', async () => {
  const requestDisplayMode = vi.fn();
  window.openai = { callTool: vi.fn(), requestDisplayMode, availableDisplayModes: ['inline'], displayMode: 'inline' };
  render(<QuestionWidget initialQuestion={ready} />);
  await waitFor(() => expect(screen.getByRole('radio', { name: /Alternativa A/ })).toBeEnabled());
  await act(async () => window.dispatchEvent(new CustomEvent('openai:set_globals', { detail: { globals: { theme: 'dark' } } })));
  expect(screen.queryByRole('button', { name: 'Expandir para estudar' })).not.toBeInTheDocument();
  await act(async () => window.dispatchEvent(new CustomEvent('openai:set_globals', { detail: { globals: { displayMode: 'fullscreen', availableDisplayModes: ['inline', 'fullscreen'] } } })));
  expect(screen.getByRole('button', { name: 'Voltar ao chat' })).toBeEnabled();
  expect(requestDisplayMode).not.toHaveBeenCalled();
});

test('fullscreen inicial com somente inline mantém retorno ao chat', async () => {
  const post = await connectHost(false, ready, {}, { displayMode: 'fullscreen', availableDisplayModes: ['inline'] });
  const button = await screen.findByRole('button', { name: 'Voltar ao chat' });
  await userEvent.click(button);
  await waitFor(() => expect(post.mock.calls.some(([m]) => m.method === 'ui/request-display-mode')).toBe(true));
  const request = post.mock.calls.find(([m]) => m.method === 'ui/request-display-mode')![0];
  expect(request.params).toEqual({ mode: 'inline' });
  await hostMessage({ jsonrpc: '2.0', id: request.id, result: { mode: 'inline' } });
  expect(screen.getByRole('main')).toHaveAttribute('data-display-mode', 'inline');
  expect(screen.queryByRole('button', { name: 'Expandir para estudar' })).not.toBeInTheDocument();
});

test('remoção externa de fullscreen mantém retorno inline permitido', async () => {
  await connectHost(false, ready, {}, { displayMode: 'fullscreen', availableDisplayModes: ['inline', 'fullscreen'] });
  await hostMessage({ jsonrpc: '2.0', method: 'ui/notifications/host-context-changed', params: { availableDisplayModes: ['inline'] } });
  expect(screen.getByRole('button', { name: 'Voltar ao chat' })).toBeEnabled();
});
