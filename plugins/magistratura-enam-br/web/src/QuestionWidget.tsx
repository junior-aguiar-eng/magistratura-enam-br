import { useEffect, useRef, useState } from "react";
import { readQuestion, type OptionId, type Question, type QuestionHost, type QuestionPresentation, type ToolResult } from "./contracts";
import { restoreUiState, type QuestionUiState } from "./question-ui-state";
import { createQuestionHost } from "./mcp-host";
import { buildFollowUp, type FollowUpAction } from "./question-followup";

const followUpLabels: Record<FollowUpAction, string> = {
  explain_error: "Explique meu erro",
  deepen_distinction: "Aprofunde esta distinção",
  new_question: "Outra questão sobre este ponto",
};

function initialUiState(question?: Question) {
  if (!question) return undefined;
  let raw: unknown;
  try { raw = window.openai?.widgetState; } catch { /* Storage is optional. */ }
  return restoreUiState(raw, question);
}

function sourceUrl(url?: string) {
  if (!url) return undefined;
  try { const parsed = new URL(url); return ["https:", "http:"].includes(parsed.protocol) ? parsed.href : undefined; }
  catch { return undefined; }
}

export function QuestionWidget({ initialQuestion = window.openai?.toolOutput }: { initialQuestion?: Question }) {
  const [question, setQuestion] = useState<Question | undefined>(() => {
    if (!initialQuestion) return undefined;
    try { return readQuestion({ structuredContent: initialQuestion }); } catch { return undefined; }
  });
  const [ui, setUi] = useState<QuestionUiState | undefined>(() => initialUiState(question));
  const uiRef = useRef(ui);
  const selected = ui?.selected_option;
  const [presentation, setPresentation] = useState<QuestionPresentation>({ displayMode: "inline", availableDisplayModes: [] });
  const [displayPending, setDisplayPending] = useState(false);
  const displayPendingRef = useRef(false);
  const [displayError, setDisplayError] = useState(false);
  const [status, setStatus] = useState<"ready" | "sending" | "error">(initialQuestion && !question ? "error" : "ready");
  const resultRef = useRef<HTMLDivElement>(null);
  const hostRef = useRef<QuestionHost | null>(null);
  const activeRef = useRef(false);
  const currentRef = useRef(question);
  const sendingRef = useRef(new Set<string>());
  const [connected, setConnected] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const uncertainRef = useRef(new Set<string>());
  const [connectionError, setConnectionError] = useState(false);
  const followUpPending = useRef(new Set<string>());
  const [followUpState, setFollowUpState] = useState<{ sessionId: string; status: "sending" | "sent" | "copy" | "error"; text?: string }>();

  function receiveResult(result: ToolResult) {
    if (!activeRef.current) return;
    const incoming = readQuestion(result);
    const current = currentRef.current;
    const rank = { ready: 0, answered: 1, invalidated: 2 };
    if (incoming.session_id === current?.session_id && rank[incoming.state] < rank[current.state]) return;
    if (incoming.session_id !== currentRef.current?.session_id) {
      setStatus("ready");
      setFollowUpState(undefined);
    }
    if (incoming.state === "invalidated" && current?.state !== "invalidated") setFollowUpState(undefined);
    const snapshot = incoming.session_id === current?.session_id ? uiRef.current : hostRef.current?.readUiState();
    const restored = restoreUiState(snapshot, incoming);
    uiRef.current = restored;
    setUi(restored);
    if (current && (incoming.session_id !== current.session_id || incoming.state !== current.state)) hostRef.current?.saveUiState(restored);
    currentRef.current = incoming;
    if (incoming.state !== "ready") uncertainRef.current.delete(incoming.session_id);
    const blocked = uncertainRef.current.has(incoming.session_id);
    setUncertain(blocked);
    if (blocked) setStatus("error");
    else if (incoming.session_id !== current?.session_id || incoming.state !== "ready" || !sendingRef.current.has(incoming.session_id)) setStatus("ready");
    setQuestion(incoming);
  }

  useEffect(() => {
    activeRef.current = true;
    const host = createQuestionHost(result => {
      if (!activeRef.current) return;
      try { receiveResult(result); } catch { setStatus("error"); }
    }, value => { if (activeRef.current) setPresentation(value); });
    hostRef.current = host;
    if (currentRef.current) host.bindSession(currentRef.current.session_id);
    host.connect().then(() => {
      if (activeRef.current && hostRef.current === host) setConnected(true);
    }).catch(() => { if (activeRef.current && hostRef.current === host) setConnectionError(true); });
    return () => { activeRef.current = false; hostRef.current = null; host.close(); };
  }, []);

  useEffect(() => { if (question?.state === "answered") resultRef.current?.focus(); }, [question?.session_id, question?.state]);

  function changeUi(change: Partial<QuestionUiState>) {
    const current = currentRef.current;
    if (!current || !uiRef.current) return;
    const next = restoreUiState({ ...uiRef.current, ...change }, current);
    uiRef.current = next;
    setUi(next);
    hostRef.current?.saveUiState(next);
  }

  function togglePanel(panel: "distractors" | "sources", open: boolean, sessionId: string) {
    if (currentRef.current?.session_id !== sessionId || currentRef.current.state !== "answered" || !uiRef.current || uiRef.current.expanded[panel] === open) return;
    changeUi({ expanded: { ...uiRef.current.expanded, [panel]: open } });
  }

  async function changeDisplayMode() {
    const host = hostRef.current;
    if (!host || !connected || displayPendingRef.current) return;
    displayPendingRef.current = true;
    setDisplayPending(true);
    setDisplayError(false);
    try { await host.requestDisplayMode(presentation.displayMode === "fullscreen" ? "inline" : "fullscreen"); }
    catch { if (activeRef.current && hostRef.current === host) setDisplayError(true); }
    finally {
      displayPendingRef.current = false;
      if (activeRef.current && hostRef.current === host) setDisplayPending(false);
    }
  }

  if (!question) return <main className="shell" aria-live="polite">{connectionError || status === "error" ? "Não foi possível carregar a questão. Reabra o card ou continue pelo chat." : "Carregando questão…"}</main>;
  const answered = question.state === "answered";
  const invalidated = question.state === "invalidated";
  const actions: FollowUpAction[] = invalidated ? ["new_question"] : answered
    ? [...(question.result === "incorrect" ? ["explain_error" as const] : []), "deepen_distinction", "new_question"] : [];
  const followUp = followUpState?.sessionId === question.session_id ? followUpState : undefined;

  async function requestFollowUp(action: FollowUpAction) {
    const host = hostRef.current;
    if (!question || !host || !connected || followUpPending.current.has(question.session_id)) return;
    const sessionId = question.session_id;
    const stillCurrent = () => activeRef.current && hostRef.current === host && currentRef.current?.session_id === sessionId;
    followUpPending.current.add(sessionId);
    setFollowUpState({ sessionId, status: "sending" });
    try {
      const snapshot = await host.callTool("obter_questao", { session_id: sessionId });
      if (!stillCurrent()) return;
      const latest = readQuestion(snapshot);
      if (latest.session_id !== sessionId || latest.state === "ready") throw new Error("Estado não confirmado");
      receiveResult(snapshot);
      const request = buildFollowUp(currentRef.current!, action);
      if (!host.capabilities.messages) {
        setFollowUpState({ sessionId, status: "copy", text: request.text });
        return;
      }
      if (host.capabilities.context) {
        try { await host.updateContext(request.context); } catch { /* The message carries its own session and action. */ }
      }
      if (!stillCurrent()) return;
      // State may change while context is being acknowledged by the host.
      const currentRequest = buildFollowUp(currentRef.current!, action);
      await host.sendMessage(currentRequest.text, sessionId);
      if (stillCurrent()) setFollowUpState({ sessionId, status: "sent" });
    } catch {
      if (stillCurrent()) setFollowUpState({ sessionId, status: "error" });
    } finally { followUpPending.current.delete(sessionId); }
  }

  async function answer() {
    if (!selected || question?.state !== "ready" || sendingRef.current.has(question.session_id) || uncertainRef.current.has(question.session_id) || !connected || !hostRef.current) return;
    const sessionId = question.session_id;
    sendingRef.current.add(sessionId);
    const host = hostRef.current;
    setStatus("sending");
    try {
      const response = await host.callTool("responder_questao", { session_id: sessionId, alternativa: selected });
      if (!activeRef.current || hostRef.current !== host) return;
      const updated = readQuestion(response);
      if (updated.session_id !== sessionId || !["answered", "invalidated"].includes(updated.state)) throw new Error("Resposta divergente");
      if (currentRef.current?.session_id === sessionId && currentRef.current.state !== "invalidated") receiveResult(response);
      if (currentRef.current?.session_id === sessionId) setStatus("ready");
    } catch {
      if (!activeRef.current || hostRef.current !== host || currentRef.current?.session_id !== sessionId) return;
      if (currentRef.current.state !== "ready") return;
      setStatus("error");
      uncertainRef.current.add(sessionId);
      setUncertain(true);
      try {
        const snapshot = await host.callTool("renderizar_questao", { session_id: sessionId });
        if (!activeRef.current || hostRef.current !== host || currentRef.current?.session_id !== sessionId) return;
        const updated = readQuestion(snapshot);
        if (updated.session_id === sessionId && updated.state !== "ready") receiveResult(snapshot);
      } catch { /* Keep the attempt blocked until an authoritative result arrives. */ }
    }
    finally { sendingRef.current.delete(sessionId); }
  }

  const canExpand = presentation.availableDisplayModes.includes("inline") && presentation.availableDisplayModes.includes("fullscreen");
  return <main className="shell" data-display-mode={presentation.displayMode}>
    {canExpand && <div className="study-toolbar"><button className="display-toggle" disabled={!connected || displayPending} aria-busy={displayPending} onClick={() => void changeDisplayMode()}>{presentation.displayMode === "fullscreen" ? "Voltar ao chat" : "Expandir para estudar"}</button></div>}
    {displayError && <p role="alert">Não foi possível mudar a apresentação. Você pode tentar novamente.</p>}
    <div className="accent" />
    <header>
      <span className="badge">Estudo Jurídico</span>
      <span className="meta"><span className="subject">{question.subject}</span><span aria-hidden="true"> · </span><span className="topic">{question.topic}</span></span>
    </header>
    {question.source_status === "caution" && <aside role="alert" className="caution"><strong>Cuidado:</strong> {question.caution_notice}</aside>}
    <h1>{question.prompt}</h1>
    {invalidated && <aside role="alert" className="caution"><strong>Questão invalidada.</strong><p>{question.invalidation_reason}</p><p>Esta questão não conta para seu desempenho.</p></aside>}
    <fieldset disabled={answered || invalidated || uncertain || status === "sending" || !connected}><legend className="sr-only">Alternativas</legend>
      {question.alternatives.map(option => <label key={option.id} className={`option ${selected === option.id ? "selected" : ""} ${answered && option.id === question.correct_option ? "correct" : ""} ${answered && option.id === question.selected_option && question.result === "incorrect" ? "incorrect" : ""}`}>
        <input type="radio" name="answer" value={option.id} checked={answered ? question.selected_option === option.id : selected === option.id} onChange={() => changeUi({ selected_option: option.id as OptionId })} />
        <span className="letter">{option.id}</span><span>{option.text}</span>
      </label>)}
    </fieldset>
    {!answered && !invalidated && <button onClick={answer} disabled={!selected || uncertain || status === "sending" || !connected}>{status === "sending" ? "Corrigindo…" : "Responder"}</button>}
    {connectionError && <p role="alert">Não foi possível conectar o card. Reabra a questão ou continue pelo chat.</p>}
    <p className="status" aria-live="polite">{status === "error" ? uncertain ? "Não foi possível confirmar sua resposta. Aguarde a atualização ou reabra o card para consultar o estado." : "Não foi possível registrar a resposta. Reabra o card ou continue pelo chat." : status === "sending" ? "Registrando sua resposta…" : ""}</p>
    {answered && <section ref={resultRef} tabIndex={-1} className={`result ${question.result}`} aria-live="polite">
      <h2>{question.result === "correct" ? "Resposta correta" : `Resposta incorreta · gabarito ${question.correct_option}`}</h2>
      <p>{question.correction?.correct_rationale}</p>
      {!!question.correction?.distractor_analysis.length && <details open={ui?.expanded.distractors ?? false} onToggle={event => togglePanel("distractors", event.currentTarget.open, question.session_id)}><summary>Análise das demais alternativas</summary>{question.correction.distractor_analysis.map(item => <p key={item.option}><strong>{item.option}:</strong> {item.analysis}</p>)}</details>}
      {!!question.correction?.exceptions.length && <div><h3>Exceções e limites</h3>{question.correction.exceptions.map((text, i) => <p key={i}>{text}</p>)}</div>}
      {!!question.correction?.traps.length && <div><h3>Armadilhas de prova</h3>{question.correction.traps.map((text, i) => <p key={i}>{text}</p>)}</div>}
      {!!question.sources?.length && <details open={ui?.expanded.sources ?? false} onToggle={event => togglePanel("sources", event.currentTarget.open, question.session_id)}><summary>Fontes da correção</summary>{question.sources.map((source, i) => <div key={`${source.source_id}-${i}`}>
        <p>{sourceUrl(source.url) ? <a href={sourceUrl(source.url)} target="_blank" rel="noreferrer noopener">{source.title}</a> : <strong>{source.title}</strong>}{source.relative_path && <> — {source.relative_path}</>}</p>
        {source.excerpt && <blockquote>{source.excerpt}</blockquote>}
        <small>Consulta: {source.accessed_at.slice(0, 10)}</small>
      </div>)}</details>}
    </section>}
    {actions.length > 0 && <section aria-label="Continuar o estudo" className="followup">
      <div className="followup-actions">{actions.map(action => <button key={action} disabled={!connected || followUp?.status === "sending"} onClick={() => void requestFollowUp(action)}>{followUpLabels[action]}</button>)}</div>
      <p role="status">{followUp?.status === "sending" ? "Preparando pedido…" : followUp?.status === "sent" ? "Pedido enviado ao chat." : followUp?.status === "copy" ? "Copie este pedido e envie no chat." : ""}</p>
      {followUp?.status === "error" && <p role="alert">Não foi possível enviar o pedido. Você pode tentar novamente.</p>}
      {followUp?.status === "copy" && <textarea aria-label="Pedido para copiar no chat" readOnly rows={5} value={followUp.text} onFocus={event => event.target.select()} />}
    </section>}
  </main>;
}
