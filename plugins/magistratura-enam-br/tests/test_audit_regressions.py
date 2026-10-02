import copy
from datetime import date

import pytest
from perfil_candidato import reconstruir_perfil
from relatorio_aprendizagem import gerar_relatorio
from test_mcp_question_sessions import sessao

from mcp_server.config import LibraryConfig
from mcp_server.tools import StudyService


@pytest.fixture
def service(tmp_path):
    (tmp_path / '.estudo-juridico').mkdir()
    (tmp_path / 'civil.md').write_text('# Civil\nConteúdo jurídico.', encoding='utf-8')
    return StudyService(LibraryConfig(tmp_path, ('.estudo-juridico',), 2_000_000, 12))


@pytest.mark.parametrize('option', ['A', 'C'])
def test_letra_nao_presume_diagnostico_dominio_assistencia_ou_versao(service, option):
    public = service.questions.create_session(sessao())
    service.answer_question(public['session_id'], option)
    event = service.questions.learning_events_store.read_all()[0]
    assert event['performance']['error_types'] == []
    assert event['performance']['domain_evidence'] == []
    assert event['activity']['assistance_level'] == 'nao_registrada'
    assert 'source_version' not in event['content_ref']
    assert event['performance']['result'] == ('correto' if option == 'C' else 'incorreto')


@pytest.mark.parametrize('broken', ['{broken', '[]', '{"documents": [null]}'])
def test_reconstroi_indice_invalido_somente_com_confirmacao(service, broken):
    service.index_path.write_text(broken, encoding='utf-8')
    with pytest.raises(PermissionError):
        service.index_library(confirmed=False)
    assert service.index_path.read_text(encoding='utf-8') == broken
    assert service.index_library(confirmed=True)['document_count'] == 1
    assert service.diagnose_library()['index_status'] == 'available'


@pytest.mark.parametrize('mutation', ['duplicate', 'correct', 'no_sources'])
def test_rejeita_correcao_incoerente_e_verificada_sem_fontes(service, mutation):
    question = sessao()
    if mutation == 'duplicate':
        question['correction']['distractor_analysis'][1]['option'] = 'A'
    elif mutation == 'correct':
        question['correction']['distractor_analysis'][1]['option'] = 'C'
    else:
        question['sources'] = []
    with pytest.raises(ValueError):
        service.questions.create_session(question)
    assert not service.questions.questions_path.exists()


def test_invalidacao_pos_tentativa_preserva_log_e_remove_efeitos(service):
    public = service.questions.create_session(sessao())
    service.answer_question(public['session_id'], 'C')
    original = service.questions.attempts_store.path.read_bytes()
    invalid = service.questions.invalidate(public['session_id'], reason='Duas respostas defensáveis', invalidated_at='2026-10-02T19:00:00Z')
    assert invalid['state'] == 'invalidated'
    assert invalid['invalidation_reason'] == 'Duas respostas defensáveis'
    assert 'correct_option' not in invalid
    assert service.questions.attempts_store.path.read_bytes() == original
    assert service.questions.get_session(public['session_id']) == invalid
    history = service.history(limit=20, cursor=0)['items'][0]
    assert history['state'] == 'invalidated'
    assert history['result'] is None
    events = service.questions.learning_events_store.read_all()
    assert len(events) == 2
    assert reconstruir_perfil(events)['competencies'] == []
    # A invalidação posterior também deve retirar a tentativa de um relatório antigo.
    assert gerar_relatorio(events, (date(2020, 1, 1), date(2030, 1, 1)))['tentativas'] == 0


def test_historico_respeita_invalidacao_antes_da_resposta(service):
    service.questions.create_session(sessao())
    service.questions.invalidate(sessao()['session_id'], reason='Ambígua', invalidated_at='2026-10-02T19:00:00Z')
    assert service.history(limit=20, cursor=0)['items'][0]['state'] == 'invalidated'


def test_invalidacao_retry_reconcilia_evento_sem_duplicar(service, monkeypatch):
    repo = service.questions
    repo.create_session(sessao())
    repo.answer(sessao()['session_id'], 'A', answered_at='2026-09-05T18:05:00Z')
    append = repo.learning_events_store.append
    def fail(_):
        raise OSError('evento indisponível')
    monkeypatch.setattr(repo.learning_events_store, 'append', fail)
    with pytest.raises(OSError):
        repo.invalidate(sessao()['session_id'], reason='Ambígua', invalidated_at='2026-10-02T19:00:00Z')
    monkeypatch.setattr(repo.learning_events_store, 'append', append)
    for _ in range(2):
        repo.invalidate(sessao()['session_id'], reason='Ambígua', invalidated_at='2026-10-02T19:01:00Z')
    assert len(repo.learning_events_store.read_all()) == 2
    assert len(repo.state_events_store.read_all()) == 1
    events = repo.learning_events_store.read_all()
    assert gerar_relatorio(events, (date(2026, 9, 1), date(2026, 9, 30)))['tentativas'] == 0


def test_retry_aceita_evento_legado_sem_reescrever_historico(service):
    repo = service.questions
    repo.create_session(sessao())
    repo.answer(sessao()['session_id'], 'A', answered_at='2026-09-05T18:05:00Z')
    event = copy.deepcopy(repo.learning_events_store.read_all()[0])
    event['schema_version'] = '2.0.0'
    event['content_ref']['source_version'] = '2026-09-05'
    event['activity']['assistance_level'] = 'nenhuma'
    event['performance']['error_types'] = ['distincao']
    event['performance']['domain_evidence'] = ['evocacao_regra']
    import json
    repo.learning_events_store.path.write_text(json.dumps(event) + '\n', encoding='utf-8')
    before = repo.learning_events_store.path.read_bytes()
    assert repo.answer(sessao()['session_id'], 'A', answered_at='2026-09-05T18:06:00Z')['result'] == 'incorrect'
    assert repo.learning_events_store.path.read_bytes() == before


def test_reconstrucao_preserva_indice_invalido_se_leitura_falhar(service, monkeypatch):
    service.index_path.write_bytes(b'{broken')
    def fail(*args, **kwargs):
        raise OSError('biblioteca indisponível')
    monkeypatch.setattr('mcp_server.tools.index_library', fail)
    with pytest.raises(OSError):
        service.index_library(confirmed=True)
    assert service.index_path.read_bytes() == b'{broken'


def test_projecao_invalidada_obedece_schema(service):
    from jsonschema import Draft202012Validator
    repo = service.questions
    repo.create_session(sessao())
    result = repo.invalidate(sessao()['session_id'], reason='Ambígua', invalidated_at='2026-10-02T19:00:00Z')
    Draft202012Validator(repo.questions_store.schema).validate(result)


@pytest.mark.anyio
async def test_invalidacao_disponivel_por_cliente_mcp(service):
    from mcp.client import Client

    from mcp_server.server import build_server
    question = sessao()
    for key in ('session_id', 'created_at', 'state', 'projection', 'schema_version'):
        question.pop(key)
    async with Client(build_server(service.config)) as client:
        created = await client.call_tool('criar_sessao_questao', {'questao': question})
        session_id = created.structured_content['session_id']
        await client.call_tool('responder_questao', {'session_id': session_id, 'alternativa': 'A'})
        invalidated = await client.call_tool('invalidar_questao', {'session_id': session_id, 'motivo': 'Duas respostas possíveis'})
        assert invalidated.structured_content['state'] == 'invalidated'
        history = await client.call_tool('consultar_historico_questoes', {})
        assert history.structured_content['items'][0]['result'] is None


def test_invalidacao_nao_exclui_outra_atividade_do_mesmo_conteudo(service):
    from eventos_aprendizagem import eventos_efetivos
    service.questions.create_session(sessao())
    service.answer_question(sessao()['session_id'], 'C')
    event = service.questions.learning_events_store.read_all()[0]
    other = copy.deepcopy(event)
    other['event_id'] = 'evt_' + 'b' * 32
    other['activity']['activity_id'] += '-outra'
    invalid = copy.deepcopy(event)
    invalid['event_id'] = 'evt_' + 'a' * 32
    invalid['performance']['result'] = 'questao_invalida'
    assert eventos_efetivos([event, other, invalid]) == [other]
