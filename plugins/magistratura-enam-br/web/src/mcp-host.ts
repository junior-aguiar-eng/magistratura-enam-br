import { App } from "@modelcontextprotocol/ext-apps";
import { normalizeToolResult, readQuestion, type Question, type QuestionHost, type ToolResult } from "./contracts";

const CALL_TIMEOUT = 30000;
const SESSION_ID = /^qsn_[0-9a-f]{16,64}$/;
const rank = { ready: 0, answered: 1, invalidated: 2 };

export function createQuestionHost(onResult: (result: ToolResult) => void): QuestionHost {
  const app = new App({ name: "estudo-juridico-question-widget", version: "0.1.0" }, {}, { autoResize: false });
  let closed = false;
  let sdkActive = true;
  let transport: "sdk" | "openai" | undefined;
  let legacy: Window["openai"];
  let connection: Promise<void> | undefined;
  let expectedSession: string | undefined;
  let delivered: Question | undefined;
  const retired = new Set<string>();
  const capabilities = { messages: false, context: false };
  const pendingLegacy = new Set<(error: Error) => void>();
  let observer: ResizeObserver | undefined;
  let resizeFrame: number | undefined;
  let previousSize: { width: number; height: number } | undefined;

  function bindSession(sessionId: string) {
    if (closed || !SESSION_ID.test(sessionId) || retired.has(sessionId)) return;
    if (expectedSession && sessionId !== expectedSession) {
      retired.add(expectedSession);
      delivered = undefined;
    }
    expectedSession = sessionId;
  }

  function receiveInput(raw: unknown) {
    if (!raw || typeof raw !== "object") return;
    const args = raw as Record<string, unknown>;
    if (Object.keys(args).length === 1 && typeof args.session_id === "string") bindSession(args.session_id);
  }

  function receiveResult(raw: unknown) {
    if (closed) return;
    let result: ToolResult;
    try { result = normalizeToolResult(raw); } catch { return; }
    if (result.isError) { onResult(result); return; }
    let incoming: Question;
    try { incoming = readQuestion(result); } catch { return; }
    if (retired.has(incoming.session_id) || (expectedSession && incoming.session_id !== expectedSession)) return;
    if (delivered && rank[incoming.state] < rank[delivered.state]) return;
    bindSession(incoming.session_id);
    delivered = incoming;
    onResult(result);
  }

  app.ontoolinput = params => { if (sdkActive && !closed) receiveInput(params.arguments); };
  app.ontoolresult = params => { if (sdkActive && !closed) receiveResult(params); };

  function receiveGlobals(event: Event) {
    if (closed || transport !== "openai") return;
    const globals = (event as CustomEvent).detail?.globals;
    if (!globals) return;
    if (globals.toolInput !== undefined) receiveInput(globals.toolInput);
    if (globals.toolOutput !== undefined) receiveResult({ structuredContent: globals.toolOutput });
  }

  function setupResize() {
    if (typeof ResizeObserver === "undefined") return;
    const schedule = () => {
      if (closed || resizeFrame !== undefined) return;
      resizeFrame = requestAnimationFrame(() => {
        resizeFrame = undefined;
        if (closed) return;
        const root = document.documentElement;
        const previousHeight = root.style.height;
        root.style.height = "max-content";
        const height = Math.ceil(root.getBoundingClientRect().height);
        root.style.height = previousHeight;
        const size = { width: Math.ceil(window.innerWidth), height };
        if (size.width !== previousSize?.width || size.height !== previousSize?.height) {
          previousSize = size;
          void app.sendSizeChanged(size).catch(() => {});
        }
      });
    };
    observer = new ResizeObserver(schedule);
    observer.observe(document.documentElement);
    observer.observe(document.body);
    schedule();
  }

  async function negotiate() {
    try {
      await app.connect(undefined, { timeout: 10000 });
      if (closed) throw new Error("Host encerrado");
      const hostCapabilities = app.getHostCapabilities();
      if (!hostCapabilities?.serverTools) throw new Error("Host sem ferramentas MCP");
      transport = "sdk";
      capabilities.messages = Boolean(hostCapabilities.message);
      capabilities.context = Boolean(hostCapabilities.updateModelContext);
      setupResize();
      return;
    } catch (error) {
      sdkActive = false;
      await app.close();
      if (closed) throw new Error("Host encerrado");
      if (!window.openai?.callTool) throw error;
    }
    legacy = window.openai;
    transport = "openai";
    capabilities.messages = Boolean(legacy?.sendFollowUpMessage);
    window.addEventListener("openai:set_globals", receiveGlobals);
    receiveInput(legacy?.toolInput);
    if (legacy?.toolOutput) receiveResult({ structuredContent: legacy.toolOutput });
  }

  async function legacyCall(name: string, args: Record<string, unknown>) {
    let timer: ReturnType<typeof setTimeout> | undefined;
    let rejectPending: (error: Error) => void = () => {};
    const cancelled = new Promise<never>((_, reject) => {
      rejectPending = reject;
      pendingLegacy.add(reject);
      timer = setTimeout(() => reject(new Error("Tempo de resposta excedido")), CALL_TIMEOUT);
    });
    try {
      return await Promise.race([legacy!.callTool!(name, args), cancelled]);
    } finally {
      clearTimeout(timer);
      pendingLegacy.delete(rejectPending);
    }
  }

  return {
    capabilities,
    bindSession,
    connect() {
      if (closed) return Promise.reject(new Error("Host encerrado"));
      return connection ??= negotiate();
    },
    async callTool(name, args) {
      if (closed || !transport) throw new Error("Conexão indisponível");
      if (typeof args.session_id === "string" && expectedSession && args.session_id !== expectedSession) {
        throw new Error("Sessão divergente da entrada do host");
      }
      // Selection is fixed before tools/call. Never retry a dispatched call
      // through a different bridge, including on timeout or transport errors.
      const result = transport === "sdk"
        ? await app.callServerTool({ name, arguments: args }, { timeout: CALL_TIMEOUT })
        : await legacyCall(name, args);
      if (closed) throw new Error("Host encerrado");
      if (typeof args.session_id === "string" && expectedSession && args.session_id !== expectedSession) {
        throw new Error("Resultado de sessão anterior");
      }
      return normalizeToolResult(result);
    },
    close() {
      if (closed) return;
      closed = true;
      sdkActive = false;
      window.removeEventListener("openai:set_globals", receiveGlobals);
      observer?.disconnect();
      if (resizeFrame !== undefined) cancelAnimationFrame(resizeFrame);
      for (const reject of pendingLegacy) reject(new Error("Host encerrado"));
      pendingLegacy.clear();
      void app.close().catch(() => {});
    },
  };
}
