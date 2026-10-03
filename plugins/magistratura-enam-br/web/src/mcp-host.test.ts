import { waitFor } from "@testing-library/react";
import { createQuestionHost } from "./mcp-host";
import type { Question } from "./contracts";

const ready: Question = { session_id: "qsn_1234567890abcdef", projection: "public", state: "ready", subject: "Civil", topic: "Prova", prompt: "Escolha.", alternatives: (["A", "B", "C", "D", "E"] as const).map(id => ({ id, text: id })), source_status: "partial" };
const next: Question = { ...ready, session_id: "qsn_abcdef1234567890", prompt: "Outra sessão." };

async function message(data: unknown) {
  window.dispatchEvent(new MessageEvent("message", { source: window.parent, data }));
  for (let i = 0; i < 12; i++) await Promise.resolve();
}

beforeEach(() => {
  window.openai = undefined;
  vi.stubGlobal("ResizeObserver", class { observe() {} disconnect() {} });
});
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

async function sdkHost(legacy = false, serverTools = true, extraCapabilities: Record<string, unknown> = {}) {
  const receive = vi.fn();
  const callTool = vi.fn().mockResolvedValue({ structuredContent: ready });
  if (legacy) window.openai = { callTool };
  const post = vi.spyOn(window.parent, "postMessage").mockImplementation(() => {});
  const host = createQuestionHost(receive);
  const connected = host.connect();
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "ui/initialize" }), "*"));
  const initialize = post.mock.calls.find(([m]) => m.method === "ui/initialize")![0];
  await message({ jsonrpc: "2.0", id: initialize.id, result: { protocolVersion: "2026-01-26", hostInfo: { name: "test", version: "1" }, hostCapabilities: { ...(serverTools ? { serverTools: {} } : {}), ...extraCapabilities }, hostContext: {} } });
  await connected;
  return { host, post, receive, callTool };
}

test.each([false, true])("SDK real recebe prioridade com bridge legado=%s", async legacy => {
  const { host, post, callTool } = await sdkHost(legacy);
  const pending = host.callTool("renderizar_questao", { session_id: ready.session_id });
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "tools/call" }), "*"));
  const request = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  await message({ jsonrpc: "2.0", id: request.id, result: { content: [], structuredContent: ready, _meta: { secret: "hidden" } } });
  expect(await pending).toEqual({ structuredContent: ready });
  expect(callTool).not.toHaveBeenCalled();
  host.close();
});

test("SDK envia mensagem e substitui contexto por payload mínimo", async () => {
  const { host, post } = await sdkHost(true, true, { message: {}, updateModelContext: {} });
  host.bindSession(ready.session_id);
  const context = { schema_version: "1.0.0" as const, session_id: ready.session_id, action: "new_question" as const, subject: ready.subject, topic: ready.topic, state: "answered" as const };
  for (const action of ["new_question", "deepen_distinction"] as const) {
    const updating = host.updateContext({ ...context, action });
    await waitFor(() => expect(post.mock.calls.map(([m]) => m).filter(m => m.method === "ui/update-model-context")).toHaveLength(action === "new_question" ? 1 : 2));
    const request = post.mock.calls.map(([m]) => m).filter(m => m.method === "ui/update-model-context").at(-1)!;
    expect(request.params.structuredContent).toEqual({ ...context, action });
    await message({ jsonrpc: "2.0", id: request.id, result: {} });
    await updating;
  }
  const sending = host.sendMessage("Pedido autossuficiente");
  await waitFor(() => expect(post.mock.calls.some(([m]) => m.method === "ui/message")).toBe(true));
  const request = post.mock.calls.find(([m]) => m.method === "ui/message")![0];
  expect(request.params).toMatchObject({ role: "user", content: [{ type: "text", text: "Pedido autossuficiente" }] });
  await message({ jsonrpc: "2.0", id: request.id, result: { isError: true } });
  await expect(sending).rejects.toThrow();
  host.close();
});

test("host sem capacidade não envia mensagem ou contexto", async () => {
  const { host, post } = await sdkHost();
  await expect(host.sendMessage("Pedido")).rejects.toThrow();
  expect(post.mock.calls.some(([m]) => m.method === "ui/message")).toBe(false);
  host.close();
});

test("host sem serverTools seleciona legado antes de qualquer envio", async () => {
  const { host, callTool, post } = await sdkHost(true, false);
  await host.callTool("renderizar_questao", { session_id: ready.session_id });
  expect(callTool).toHaveBeenCalledTimes(1);
  expect(post.mock.calls.some(([m]) => m.method === "tools/call")).toBe(false);
  host.close();
});

test("falha explícita de inicialização permite somente OpenAI", async () => {
  const callTool = vi.fn().mockResolvedValue({ structured_content: ready, _meta: { secret: "hidden" } });
  window.openai = { callTool };
  const post = vi.spyOn(window.parent, "postMessage").mockImplementation(() => {});
  const host = createQuestionHost(vi.fn());
  const connection = host.connect();
  await waitFor(() => expect(post).toHaveBeenCalled());
  const initialize = post.mock.calls.find(([m]) => m.method === "ui/initialize")![0];
  await message({ jsonrpc: "2.0", id: initialize.id, error: { code: -32601, message: "MCP Apps unavailable" } });
  await connection;
  expect(await host.callTool("renderizar_questao", {})).toEqual({ structuredContent: ready });
  host.close();
});

test("entrada após aprovação não renderiza dados privados ou parciais", async () => {
  const { host, receive } = await sdkHost();
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input-partial", params: { arguments: { session_id: ready.session_id, correct_option: "C" } } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { questao: { ...ready, projection: "private", correct_option: "C" } } } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: ready.session_id } } });
  expect(receive).not.toHaveBeenCalled();
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { content: [], structuredContent: ready, _meta: { secret: "hidden" } } });
  expect(receive).toHaveBeenCalledWith({ structuredContent: ready });
  host.close();
});

test("notificação atrasada não troca a sessão atual", async () => {
  const { host, receive } = await sdkHost();
  host.bindSession(ready.session_id);
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: { session_id: ready.session_id, projection: "private" } } });
  expect(receive).toHaveBeenCalledTimes(1);
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: next } });
  expect(receive).toHaveBeenLastCalledWith({ structuredContent: next });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: ready.session_id } } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  expect(receive).toHaveBeenCalledTimes(2);
  host.close();
});

test("timeout após envio não repete mutação pelo legado", async () => {
  const { host, post, callTool } = await sdkHost(true);
  vi.useFakeTimers();
  const outcome = host.callTool("responder_questao", { session_id: ready.session_id, alternativa: "B" }).catch(error => error);
  await vi.advanceTimersByTimeAsync(30001);
  expect(await outcome).toBeInstanceOf(Error);
  expect(post.mock.calls.filter(([m]) => m.method === "tools/call" && m.params.name === "responder_questao")).toHaveLength(1);
  expect(callTool).not.toHaveBeenCalled();
  host.close();
});

test("isError permanece erro no envelope normalizado", async () => {
  const { host, post } = await sdkHost();
  const pending = host.callTool("responder_questao", {});
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "tools/call" }), "*"));
  const request = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  await message({ jsonrpc: "2.0", id: request.id, result: { content: [], isError: true, _meta: { secret: "hidden" } } });
  expect(await pending).toEqual({ isError: true });
  host.close();
});

test("close desconecta listeners e ignora notificações atrasadas", async () => {
  const disconnect = vi.fn();
  vi.stubGlobal("ResizeObserver", class { observe() {} disconnect = disconnect; });
  const remove = vi.spyOn(window, "removeEventListener");
  const { host, receive } = await sdkHost();
  host.close();
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  expect(receive).not.toHaveBeenCalled();
  expect(remove).toHaveBeenCalledWith("message", expect.any(Function));
  expect(disconnect).toHaveBeenCalledTimes(1);
  await expect(host.callTool("responder_questao", {})).rejects.toThrow();
});

test("aprovação com progresso mantém o mesmo envio até o resultado", async () => {
  const { host, post, callTool } = await sdkHost(true);
  vi.useFakeTimers();
  let settled = false;
  const pending = host.callTool("responder_questao", { session_id: ready.session_id, alternativa: "B" }).finally(() => { settled = true; });
  await vi.advanceTimersByTimeAsync(20000);
  const request = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  await message({ jsonrpc: "2.0", method: "notifications/progress", params: { progressToken: request.params._meta.progressToken, progress: 1, total: 2 } });
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: ready.session_id } } });
  await vi.advanceTimersByTimeAsync(20000);
  expect(settled).toBe(false);
  await message({ jsonrpc: "2.0", id: request.id, result: { content: [], structuredContent: ready } });
  expect(await pending).toEqual({ structuredContent: ready });
  expect(callTool).not.toHaveBeenCalled();
  host.close();
});

test("encerrar durante initialize impede fallback e resultados tardios", async () => {
  const post = vi.spyOn(window.parent, "postMessage").mockImplementation(() => {});
  const callTool = vi.fn();
  window.openai = { callTool };
  const receive = vi.fn();
  const host = createQuestionHost(receive);
  const connection = host.connect().catch(error => error);
  await waitFor(() => expect(post).toHaveBeenCalled());
  host.close();
  expect(await connection).toBeInstanceOf(Error);
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-result", params: { structuredContent: ready } });
  expect(receive).not.toHaveBeenCalled();
  expect(callTool).not.toHaveBeenCalled();
});

test("OpenAI fixado encerra chamada pendente e remove listener", async () => {
  const { host, post, receive, callTool } = await sdkHost(true, false);
  const remove = vi.spyOn(window, "removeEventListener");
  callTool.mockImplementation(() => new Promise(() => {}));
  const outcome = host.callTool("responder_questao", {}).catch(error => error);
  host.close();
  expect(await outcome).toBeInstanceOf(Error);
  expect(remove).toHaveBeenCalledWith("openai:set_globals", expect.any(Function));
  window.dispatchEvent(new CustomEvent("openai:set_globals", { detail: { globals: { toolOutput: ready } } }));
  expect(receive).not.toHaveBeenCalled();
  expect(post.mock.calls.some(([m]) => m.method === "tools/call")).toBe(false);
});

test("entrada nova impede enviar tentativa pela sessão antiga ainda visível", async () => {
  const { host, post } = await sdkHost();
  host.bindSession(ready.session_id);
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  const outcome = host.callTool("responder_questao", { session_id: ready.session_id, alternativa: "B" }).catch(error => error);
  for (let i = 0; i < 12; i++) await Promise.resolve();
  const calls = post.mock.calls.filter(([m]) => m.method === "tools/call");
  host.close();
  expect(await outcome).toBeInstanceOf(Error);
  expect(calls).toHaveLength(0);
});

test("retorno correlacionado de sessão antiga não alcança o consumidor", async () => {
  const { host, post } = await sdkHost();
  host.bindSession(ready.session_id);
  const outcome = host.callTool("responder_questao", { session_id: ready.session_id, alternativa: "B" }).catch(error => error);
  await waitFor(() => expect(post).toHaveBeenCalledWith(expect.objectContaining({ method: "tools/call" }), "*"));
  const request = post.mock.calls.find(([m]) => m.method === "tools/call")![0];
  await message({ jsonrpc: "2.0", method: "ui/notifications/tool-input", params: { arguments: { session_id: next.session_id } } });
  await message({ jsonrpc: "2.0", id: request.id, result: { content: [], structuredContent: ready } });
  expect(await outcome).toBeInstanceOf(Error);
  host.close();
});
