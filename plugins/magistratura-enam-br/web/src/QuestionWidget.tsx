import { useEffect, useRef, useState } from "react";
import { App } from "@modelcontextprotocol/ext-apps";
import { readQuestion, type OptionId, type Question, type ToolResult } from "./contracts";

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
  const [selected, setSelected] = useState<OptionId>();
  const [status, setStatus] = useState<"ready" | "sending" | "error">(initialQuestion && !question ? "error" : "ready");
  const resultRef = useRef<HTMLDivElement>(null);
  const appRef = useRef<App | null>(null);
  const currentRef = useRef(question);
  const sendingRef = useRef(false);
  const [connected, setConnected] = useState(Boolean(window.openai?.callTool));
  const [connectionError, setConnectionError] = useState(false);

  function receiveResult(result: ToolResult) {
    const incoming = readQuestion(result);
    const current = currentRef.current;
    const rank = { ready: 0, answered: 1, invalidated: 2 };
    if (incoming.session_id === current?.session_id && rank[incoming.state] < rank[current.state]) return;
    if (incoming.session_id !== currentRef.current?.session_id) {
      setSelected(undefined);
      setStatus("ready");
    }
    currentRef.current = incoming;
    if (incoming.session_id !== current?.session_id || incoming.state !== "ready" || !sendingRef.current) setStatus("ready");
    setQuestion(incoming);
  }

  useEffect(() => {
    let active = true;
    if (window.openai?.callTool) {
      const receiveGlobals = (event: Event) => {
        const output = (event as CustomEvent).detail?.globals?.toolOutput;
        if (output) {
          try { receiveResult({ structuredContent: output }); } catch { setStatus("error"); }
        }
      };
      window.addEventListener("openai:set_globals", receiveGlobals);
      return () => window.removeEventListener("openai:set_globals", receiveGlobals);
    }
    const app = new App({ name: "estudo-juridico-question-widget", version: "0.1.0" }, {});
    appRef.current = app;
    app.ontoolresult = result => {
      if (!active) return;
      try { receiveResult(result); } catch { setStatus("error"); }
    };
    app.connect(undefined, { timeout: 10000 }).then(() => {
      if (active) setConnected(true);
    }).catch(() => { if (active) setConnectionError(true); });
    return () => { active = false; appRef.current = null; void app.close(); };
  }, []);

  useEffect(() => { if (question?.state === "answered") resultRef.current?.focus(); }, [question]);

  if (!question) return <main className="shell" aria-live="polite">{connectionError || status === "error" ? "Não foi possível carregar a questão. Reabra o card ou continue pelo chat." : "Carregando questão…"}</main>;
  const answered = question.state === "answered";
  const invalidated = question.state === "invalidated";

  async function answer() {
    if (!selected || question?.state !== "ready" || sendingRef.current || !connected) return;
    sendingRef.current = true;
    const sessionId = question.session_id;
    setStatus("sending");
    try {
      let response: ToolResult;
      if (window.openai?.callTool) {
        response = await window.openai.callTool("responder_questao", { session_id: sessionId, alternativa: selected });
      } else {
        if (!appRef.current) throw new Error("Conexão indisponível");
        response = await appRef.current.callServerTool({ name: "responder_questao", arguments: { session_id: sessionId, alternativa: selected } }, { timeout: 30000 });
      }
      const updated = readQuestion(response);
      if (updated.session_id !== sessionId || !["answered", "invalidated"].includes(updated.state)) throw new Error("Resposta divergente");
      if (currentRef.current?.session_id === sessionId && currentRef.current.state !== "invalidated") receiveResult(response);
      if (currentRef.current?.session_id === sessionId) setStatus("ready");
    } catch { if (currentRef.current?.session_id === sessionId) setStatus("error"); }
    finally { sendingRef.current = false; }
  }

  return <main className="shell">
    <div className="accent" />
    <header>
      <span className="badge">Estudo Jurídico</span>
      <span className="meta"><span className="subject">{question.subject}</span><span aria-hidden="true"> · </span><span className="topic">{question.topic}</span></span>
    </header>
    {question.source_status === "caution" && <aside role="alert" className="caution"><strong>Cuidado:</strong> {question.caution_notice}</aside>}
    <h1>{question.prompt}</h1>
    {invalidated && <aside role="alert" className="caution"><strong>Questão invalidada.</strong><p>{question.invalidation_reason}</p><p>Esta questão não conta para seu desempenho.</p></aside>}
    <fieldset disabled={answered || invalidated || status === "sending" || !connected}><legend className="sr-only">Alternativas</legend>
      {question.alternatives.map(option => <label key={option.id} className={`option ${selected === option.id ? "selected" : ""} ${answered && option.id === question.correct_option ? "correct" : ""} ${answered && option.id === question.selected_option && question.result === "incorrect" ? "incorrect" : ""}`}>
        <input type="radio" name="answer" value={option.id} checked={answered ? question.selected_option === option.id : selected === option.id} onChange={() => setSelected(option.id)} />
        <span className="letter">{option.id}</span><span>{option.text}</span>
      </label>)}
    </fieldset>
    {!answered && !invalidated && <button onClick={answer} disabled={!selected || status === "sending" || !connected}>{status === "sending" ? "Corrigindo…" : "Responder"}</button>}
    {connectionError && <p role="alert">Não foi possível conectar o card. Reabra a questão ou continue pelo chat.</p>}
    <p className="status" aria-live="polite">{status === "error" ? "Não foi possível registrar a resposta. Tente novamente." : status === "sending" ? "Registrando sua resposta…" : ""}</p>
    {answered && <section ref={resultRef} tabIndex={-1} className={`result ${question.result}`} aria-live="polite">
      <h2>{question.result === "correct" ? "Resposta correta" : `Resposta incorreta · gabarito ${question.correct_option}`}</h2>
      <p>{question.correction?.correct_rationale}</p>
      {!!question.correction?.distractor_analysis.length && <details><summary>Análise das demais alternativas</summary>{question.correction.distractor_analysis.map(item => <p key={item.option}><strong>{item.option}:</strong> {item.analysis}</p>)}</details>}
      {!!question.correction?.exceptions.length && <div><h3>Exceções e limites</h3>{question.correction.exceptions.map((text, i) => <p key={i}>{text}</p>)}</div>}
      {!!question.correction?.traps.length && <div><h3>Armadilhas de prova</h3>{question.correction.traps.map((text, i) => <p key={i}>{text}</p>)}</div>}
      {!!question.sources?.length && <details><summary>Fontes da correção</summary>{question.sources.map((source, i) => <div key={`${source.source_id}-${i}`}>
        <p>{sourceUrl(source.url) ? <a href={sourceUrl(source.url)} target="_blank" rel="noreferrer noopener">{source.title}</a> : <strong>{source.title}</strong>}{source.relative_path && <> — {source.relative_path}</>}</p>
        {source.excerpt && <blockquote>{source.excerpt}</blockquote>}
        <small>Consulta: {source.accessed_at.slice(0, 10)}</small>
      </div>)}</details>}
    </section>}
  </main>;
}
