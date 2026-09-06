import { useEffect, useRef, useState } from "react";
import type { OptionId, Question } from "./contracts";

export function QuestionWidget({ initialQuestion = window.openai?.toolOutput }: { initialQuestion?: Question }) {
  const [question, setQuestion] = useState<Question | undefined>(initialQuestion);
  const [selected, setSelected] = useState<OptionId>();
  const [status, setStatus] = useState<"ready" | "sending" | "error">("ready");
  const resultRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const receive = (event: MessageEvent) => {
      if (event.data?.method !== "ui/notifications/tool-result") return;
      const params = event.data?.params;
      const payload = params?.structuredContent
        ?? params?.structured_content
        ?? params?.result?.structuredContent
        ?? params?.result?.structured_content;
      if (payload) setQuestion(payload);
    };
    window.addEventListener("message", receive);
    return () => window.removeEventListener("message", receive);
  }, []);

  useEffect(() => { if (question?.state === "answered") resultRef.current?.focus(); }, [question]);

  if (!question) return <main className="shell" aria-live="polite">Carregando questão…</main>;
  const answered = question.state === "answered";

  async function answer() {
    if (!selected || answered) return;
    setStatus("sending");
    try {
      if (window.openai?.callTool) {
        const response = await window.openai.callTool("responder_questao", { session_id: question!.session_id, alternativa: selected });
        const payload = response.structuredContent ?? response.structured_content;
        if (!payload) throw new Error("Resposta sem dados estruturados");
        setQuestion(payload);
      } else {
        window.parent.postMessage({ jsonrpc: "2.0", id: crypto.randomUUID(), method: "tools/call", params: { name: "responder_questao", arguments: { session_id: question!.session_id, alternativa: selected } } }, "*");
      }
      setStatus("ready");
    } catch { setStatus("error"); }
  }

  return <main className="shell">
    <div className="accent" />
    <header>
      <span className="badge">Estudo Jurídico</span>
      <span className="meta"><span className="subject">{question.subject}</span><span aria-hidden="true"> · </span><span className="topic">{question.topic}</span></span>
    </header>
    {question.source_status === "caution" && <aside role="alert" className="caution"><strong>Cuidado:</strong> {question.caution_notice}</aside>}
    <h1>{question.prompt}</h1>
    <fieldset disabled={answered || status === "sending"}><legend className="sr-only">Alternativas</legend>
      {question.alternatives.map(option => <label key={option.id} className={`option ${selected === option.id ? "selected" : ""} ${answered && option.id === question.correct_option ? "correct" : ""} ${answered && option.id === question.selected_option && question.result === "incorrect" ? "incorrect" : ""}`}>
        <input type="radio" name="answer" value={option.id} checked={selected === option.id || (answered && question.selected_option === option.id)} onChange={() => setSelected(option.id)} />
        <span className="letter">{option.id}</span><span>{option.text}</span>
      </label>)}
    </fieldset>
    {!answered && <button onClick={answer} disabled={!selected || status === "sending"}>{status === "sending" ? "Corrigindo…" : "Responder"}</button>}
    <p className="status" aria-live="polite">{status === "error" ? "Não foi possível registrar a resposta. Tente novamente." : status === "sending" ? "Registrando sua resposta…" : ""}</p>
    {answered && <section ref={resultRef} tabIndex={-1} className={`result ${question.result}`} aria-live="polite">
      <h2>{question.result === "correct" ? "Resposta correta" : `Resposta incorreta · gabarito ${question.correct_option}`}</h2>
      <p>{question.correction?.correct_rationale}</p>
      {!!question.correction?.distractor_analysis.length && <details><summary>Análise das demais alternativas</summary>{question.correction.distractor_analysis.map(item => <p key={item.option}><strong>{item.option}:</strong> {item.analysis}</p>)}</details>}
    </section>}
  </main>;
}
