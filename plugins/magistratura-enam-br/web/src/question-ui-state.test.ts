import { restoreUiState } from './question-ui-state';
import type { Question } from './contracts';
const question = { session_id: 'qsn_1234567890abcdef', state: 'ready' } as Question;
const snapshot = { schema_version: '1.0.0', session_id: question.session_id, selected_option: 'B', expanded: { distractors: true, sources: true } };
const empty = { schema_version: '1.0.0', session_id: question.session_id, expanded: { distractors: false, sources: false } };
test('restaura somente whitelist visual da mesma sessão', () => expect(restoreUiState(snapshot, question)).toEqual(snapshot));
test.each([null, [], {}, { ...snapshot, schema_version: '2' }, { ...snapshot, session_id: 'outra' }, { ...snapshot, correct_option: 'C' }, { ...snapshot, correction: {} }, { ...snapshot, displayMode: 'fullscreen' }, { ...snapshot, selected_option: 'F' }, { ...snapshot, expanded: { ...snapshot.expanded, sources: 'true' } }, { ...snapshot, expanded: { ...snapshot.expanded, secret: 'gabarito' } }])('rejeita snapshot adulterado %j', raw => expect(restoreUiState(raw, question)).toEqual(empty));
test('servidor answered vence seleção antiga sem persistir alternativa respondida', () => {
  expect(restoreUiState(snapshot, { ...question, state: 'answered', selected_option: 'C' })).toEqual({ ...empty, expanded: snapshot.expanded });
});
test('invalidação limpa escolha e painéis', () => expect(restoreUiState(snapshot, { ...question, state: 'invalidated' })).toEqual(empty));
test('snapshot restaurado é cópia sem referências compartilhadas', () => expect(restoreUiState(snapshot, question).expanded).not.toBe(snapshot.expanded));

test('campos herdados não constituem snapshot da whitelist', () => expect(restoreUiState(Object.create(snapshot), question)).toEqual(empty));
