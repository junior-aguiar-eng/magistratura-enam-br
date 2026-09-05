import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QuestionWidget } from "./QuestionWidget";
import "./styles.css";

const demo = new URLSearchParams(location.search).has("demo") ? {
  session_id: "qsn_1234567890abcdef", projection: "public" as const, state: "ready" as const,
  subject: "Processo Civil", topic: "Julgamento imediato do mérito", mode: "training",
  prompt: "Em ação de obrigação de fazer, o tribunal reconheceu que a prova pericial era indispensável. Considerando o Código de Processo Civil, assinale a alternativa correta.",
  alternatives: (["A", "B", "C", "D", "E"] as const).map((id) => ({ id, text: `Alternativa ${id}: formulação jurídica de alta dificuldade para análise do candidato.` })),
  source_status: "caution" as const, caution_notice: "A questão foi gerada com fontes parcialmente verificadas; confirme alterações legislativas ou jurisprudenciais recentes.",
} : undefined;

createRoot(document.getElementById("root")!).render(<StrictMode><QuestionWidget initialQuestion={demo} /></StrictMode>);
