import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QuestionWidget } from "./QuestionWidget";
import type { Question } from "./contracts";

const ready: Question = { session_id: "qsn_1234567890abcdef", projection: "public", state: "ready", subject: "Processo Civil", topic: "Provas", prompt: "Assinale a alternativa correta.", alternatives: (["A","B","C","D","E"] as const).map((id) => ({ id, text: `Alternativa ${id}` })), source_status: "caution", caution_notice: "Fontes canônicas parcialmente disponíveis." };
const corrected: Question = { ...ready, projection: "corrected", state: "answered", selected_option: "B", correct_option: "C", result: "incorrect", correction: { correct_rationale: "A alternativa C observa o CPC.", distractor_analysis: [{option:"A",analysis:"Erro A"},{option:"B",analysis:"Erro B"},{option:"D",analysis:"Erro D"},{option:"E",analysis:"Erro E"}], exceptions: [], traps: [] } };

beforeEach(() => { window.openai = { callTool: vi.fn() }; });
afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals(); });

async function hostMessage(data: unknown) {
  await act(async () => {
    window.dispatchEvent(new MessageEvent("message", { source: window, data }));
  });
}

async function connectHost() {
  vi.stubGlobal("ResizeObserver", class { observe() {} disconnect() {} });
  window.openai = undefined;
  const post = vi.spyOn(window.parent, "postMessage").mockImplementation(() => {});
  render(<QuestionWidget />);
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "ui/initialize" }), "*"));
  const initialize = post.mock.calls.find(([message]) => message.method === "ui/initialize")![0];
  await hostMessage({ jsonrpc: "2.0", id: initialize.id, result: {
    protocolVersion: "2026-01-26", hostInfo: { name: "test-host", version: "1.0" },
    hostCapabilities: { serverTools: {} }, hostContext: {},
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
