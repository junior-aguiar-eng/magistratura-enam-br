export type OptionId = "A" | "B" | "C" | "D" | "E";
export interface Source {
  source_id: string; kind: string; title: string; accessed_at: string; role: string;
  url?: string; relative_path?: string; excerpt?: string;
}
export interface Question {
  session_id: string; projection: "public" | "corrected"; state: "ready" | "answered" | "invalidated";
  subject: string; topic: string; prompt: string; alternatives: { id: OptionId; text: string }[];
  source_status: "verified" | "partial" | "caution"; caution_notice?: string;
  sources?: Source[]; invalidation_reason?: string;
  selected_option?: OptionId; correct_option?: OptionId; result?: "correct" | "incorrect";
  correction?: { correct_rationale: string; distractor_analysis: { option: OptionId; analysis: string }[]; exceptions: string[]; traps: string[] };
}

export interface ToolResult { isError?: boolean; structuredContent?: unknown; structured_content?: unknown }

export interface QuestionHost {
  readonly capabilities: { messages: boolean; context: boolean };
  bindSession(sessionId: string): void;
  connect(): Promise<void>;
  callTool(name: string, args: Record<string, unknown>): Promise<ToolResult>;
  close(): void;
}

export function normalizeToolResult(raw: unknown): ToolResult {
  if (!raw || typeof raw !== "object") throw new Error("Resultado inválido");
  const result = raw as Record<string, unknown>;
  if ((result.isError !== undefined && typeof result.isError !== "boolean")
    || (result.is_error !== undefined && typeof result.is_error !== "boolean")) throw new Error("Resultado inválido");
  const output: ToolResult = {};
  if (result.isError === true || result.is_error === true) output.isError = true;
  const value = result.structuredContent ?? result.structured_content;
  if (value !== undefined) output.structuredContent = value;
  return output;
}

function stringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === "string");
}

export function readQuestion(result: ToolResult): Question {
  const normalized = normalizeToolResult(result);
  const value = normalized.structuredContent;
  if (normalized.isError || !value || typeof value !== "object") throw new Error("Resultado inválido");
  const q = value as Question;
  if (typeof q.session_id !== "string" || typeof q.prompt !== "string"
    || typeof q.subject !== "string" || typeof q.topic !== "string"
    || !["verified", "partial", "caution"].includes(q.source_status)
    || (q.caution_notice !== undefined && typeof q.caution_notice !== "string")
    || !["ready", "answered", "invalidated"].includes(q.state)
    || !Array.isArray(q.alternatives) || q.alternatives.length !== 5
    || !q.alternatives.every((a, i) => a?.id === "ABCDE"[i] && typeof a.text === "string")) {
    throw new Error("Questão inválida");
  }
  if (q.sources !== undefined && (!Array.isArray(q.sources) || !q.sources.every(source =>
    source && typeof source === "object" && typeof source.source_id === "string"
    && typeof source.title === "string" && typeof source.accessed_at === "string"
    && (source.url === undefined || typeof source.url === "string")
    && (source.relative_path === undefined || typeof source.relative_path === "string")
    && (source.excerpt === undefined || typeof source.excerpt === "string")))) {
    throw new Error("Fontes inválidas");
  }
  if (q.state !== "answered" && (q.projection !== "public" || q.correct_option !== undefined || q.correction !== undefined
    || "selected_option" in q || "result" in q || "answered_at" in q)) {
    throw new Error("Projeção pública inválida");
  }
  if (q.state === "invalidated" && typeof q.invalidation_reason !== "string") throw new Error("Invalidação sem motivo");
  if (q.state === "answered" && (q.projection !== "corrected" || !q.correction
    || !["correct", "incorrect"].includes(q.result ?? "")
    || !["A", "B", "C", "D", "E"].includes(q.correct_option ?? "")
    || !["A", "B", "C", "D", "E"].includes(q.selected_option ?? "")
    || typeof q.correction.correct_rationale !== "string"
    || !Array.isArray(q.correction.distractor_analysis)
    || !q.correction.distractor_analysis.every(item => item && typeof item === "object"
      && ["A", "B", "C", "D", "E"].includes(item.option) && typeof item.analysis === "string")
    || !stringArray(q.correction.exceptions) || !stringArray(q.correction.traps))) {
    throw new Error("Correção inválida");
  }
  return q;
}

declare global {
  interface Window {
    openai?: {
      toolOutput?: Question; toolInput?: unknown;
      callTool?: (name: string, args: unknown) => Promise<ToolResult>;
      sendFollowUpMessage?: (args: { prompt: string }) => Promise<unknown>;
    };
  }
}
