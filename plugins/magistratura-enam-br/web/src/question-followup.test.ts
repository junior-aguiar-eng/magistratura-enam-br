import { buildFollowUp, type FollowUpAction } from "./question-followup";
import type { Question } from "./contracts";

const ready: Question = { session_id: "qsn_1234567890abcdef", projection: "public", state: "ready", subject: "Civil", topic: "Provas", prompt: "Caso privado ao contexto", alternatives: (["A","B","C","D","E"] as const).map(id => ({ id, text: id })), source_status: "partial" };
const answered: Question = { ...ready, state: "answered", projection: "corrected", selected_option: "B", correct_option: "C", result: "incorrect", correction: { correct_rationale: "Segredo da correção", distractor_analysis: [], exceptions: [], traps: [] } };
const invalidated: Question = { ...ready, state: "invalidated", invalidation_reason: "Ambígua" };

test.each<FollowUpAction>(["explain_error", "deepen_distinction", "new_question"])("não oferece %s antes da tentativa", action => {
  expect(() => buildFollowUp(ready, action)).toThrow();
});
test.each<FollowUpAction>(["explain_error", "deepen_distinction", "new_question"])("mensagem %s é autossuficiente sem payload de resposta", action => {
  const result = buildFollowUp(answered, action);
  expect(result.context).toEqual({ schema_version: "1.0.0", session_id: ready.session_id, action, subject: "Civil", topic: "Provas", state: "answered" });
  expect(result.text).toContain(ready.session_id);
  expect(result.text).toContain("obter_questao");
  expect(result.text).toContain(action);
  expect(JSON.stringify(result)).not.toMatch(/correct_option|selected_option|correction|Segredo|Caso privado/);
});
test("acerto não autoriza diagnóstico de erro", () => {
  expect(() => buildFollowUp({ ...answered, result: "correct", selected_option: "C" }, "explain_error")).toThrow();
  expect(buildFollowUp({ ...answered, result: "correct", selected_option: "C" }, "deepen_distinction").text).toContain("deepen_distinction");
});
test("invalidada permite apenas nova questão com aviso", () => {
  expect(() => buildFollowUp(invalidated, "explain_error")).toThrow();
  expect(() => buildFollowUp(invalidated, "deepen_distinction")).toThrow();
  expect(buildFollowUp(invalidated, "new_question").text).toMatch(/invalidada/);
});
