export type OptionId = "A" | "B" | "C" | "D" | "E";
export interface Question {
  session_id: string; projection: "public" | "corrected"; state: "ready" | "answered";
  subject: string; topic: string; prompt: string; alternatives: { id: OptionId; text: string }[];
  source_status: "verified" | "partial" | "caution"; caution_notice?: string;
  selected_option?: OptionId; correct_option?: OptionId; result?: "correct" | "incorrect";
  correction?: { correct_rationale: string; distractor_analysis: { option: OptionId; analysis: string }[]; exceptions: string[]; traps: string[] };
}

declare global {
  interface Window {
    openai?: { toolOutput?: Question; callTool?: (name: string, args: unknown) => Promise<{ structuredContent?: Question; structured_content?: Question }> };
  }
}
