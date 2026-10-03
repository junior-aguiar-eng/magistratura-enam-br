import type { OptionId, Question } from './contracts';
export interface QuestionUiState {
  schema_version: '1.0.0'; session_id: string; selected_option?: OptionId;
  expanded: { distractors: boolean; sources: boolean };
}
export function restoreUiState(raw: unknown, question: Question): QuestionUiState {
  const state: QuestionUiState = { schema_version: '1.0.0', session_id: question.session_id, expanded: { distractors: false, sources: false } };
  if (!raw || typeof raw !== 'object' || Array.isArray(raw) || question.state === 'invalidated') return state;
  const snapshot = raw as Record<string, unknown>;
  if (!['schema_version', 'session_id', 'expanded'].every(key => Object.hasOwn(snapshot, key))) return state;
  const allowed = ['schema_version', 'session_id', 'selected_option', 'expanded'];
  if (Object.keys(snapshot).some(key => !allowed.includes(key)) || snapshot.schema_version !== '1.0.0' || snapshot.session_id !== question.session_id) return state;
  if (snapshot.selected_option !== undefined && !['A', 'B', 'C', 'D', 'E'].includes(snapshot.selected_option as string)) return state;
  const expanded = snapshot.expanded;
  if (!expanded || typeof expanded !== 'object' || Array.isArray(expanded)) return state;
  const panels = expanded as Record<string, unknown>;
  if (Object.keys(panels).length !== 2 || Object.keys(panels).some(key => !['distractors', 'sources'].includes(key)) || typeof panels.distractors !== 'boolean' || typeof panels.sources !== 'boolean') return state;
  state.expanded = { distractors: panels.distractors, sources: panels.sources };
  if (question.state === 'ready' && snapshot.selected_option !== undefined) state.selected_option = snapshot.selected_option as OptionId;
  return state;
}
