import copy
import hashlib
import json
from pathlib import Path

import pytest


def case():
    return {
        'id': 'sintetico', 'human_rubric': ['Fundamento consistente'],
        'assertions': [{'id': 'estrutura', 'description': 'Contém o marcador', 'kind': 'automatic', 'check': 'contains_all', 'values': ['fundamento']}],
    }


def metadata():
    return {'run_id': 'run-teste-1', 'executed_at': '2026-10-02T12:00:00Z',
            'plugin_version': '0.7.4', 'model': 'modelo-de-teste', 'client': 'cliente-de-teste 1.0',
            'session_id': 'sessao-sintetica', 'round': 1, 'origin': 'synthetic_fixture'}


def review():
    return {'reviewer': 'Revisor de teste', 'reviewed_at': '2026-10-02', 'review_note': 'Revisão sintética de teste',
            'output_sha256': hashlib.sha256(b'Um fundamento.').hexdigest(),
            'case_sha256': hashlib.sha256(json.dumps(case(), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'criteria': [{'id': 'rubrica-1', 'passed': True, 'evidence': 'O texto desenvolve o fundamento.'}]}


def recorder():
    import importlib
    return importlib.import_module('registrar_execucao_pedagogica')


def test_registra_saida_e_proveniencia_sem_aprovar_direito(tmp_path):
    record = recorder().registrar_execucao(case(), 'Um fundamento.', metadata(), tmp_path / 'run.json')
    assert record['evaluation']['status'] == 'revisao_humana_pendente'
    assert record['output_sha256'] == hashlib.sha256(b'Um fundamento.').hexdigest()
    assert record['case_snapshot'] == case()
    assert json.loads((tmp_path / 'run.json').read_text(encoding='utf-8')) == record
    with pytest.raises(FileExistsError):
        recorder().registrar_execucao(case(), 'Outro fundamento.', metadata(), tmp_path / 'run.json')


def test_revisao_da_saida_exige_cobertura_integral_e_evidencia(tmp_path):
    approved = recorder().registrar_execucao(case(), 'Um fundamento.', metadata(), tmp_path / 'approved.json', revisao=review())
    assert approved['evaluation']['status'] == 'aprovado_com_revisao_humana'
    for index, mutation in enumerate((lambda r: r.update(criteria=[]), lambda r: r['criteria'][0].update(evidence=' '), lambda r: r.update(reviewer=' '))):
        invalid = copy.deepcopy(review())
        mutation(invalid)
        with pytest.raises(ValueError):
            recorder().registrar_execucao(case(), 'Um fundamento.', metadata(), tmp_path / f'invalid-{index}.json', revisao=invalid)
        assert not (tmp_path / f'invalid-{index}.json').exists()


def test_revisao_humana_nao_supera_falha_automatica(tmp_path):
    output_review = review()
    output_review['output_sha256'] = hashlib.sha256(b'Texto sem marcador.').hexdigest()
    record = recorder().registrar_execucao(case(), 'Texto sem marcador.', metadata(), tmp_path / 'failed.json', revisao=output_review)
    assert record['evaluation']['status'] == 'reprovado'


def test_fixture_pendente_nao_vira_aprovada_por_revisao_da_saida(tmp_path):
    pending = case()
    pending['legal_grounding'] = {'human_review': {'review_status': 'pending', 'review_note': ''}}
    output_review = review()
    output_review['case_sha256'] = hashlib.sha256(json.dumps(pending, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    output_review['criteria'].extend([
        {'id': 'validacao-fixture-juridica', 'passed': True, 'evidence': 'Não substitui revisão da fixture.'},
        {'id': 'aplicacao-fundamentacao-juridica', 'passed': True, 'evidence': 'Aplicação conferida.'},
    ])
    record = recorder().registrar_execucao(pending, 'Um fundamento.', metadata(), tmp_path / 'pending.json', revisao=output_review)
    assert record['evaluation']['status'] == 'revisao_humana_pendente'


@pytest.mark.parametrize('field,value', [('plugin_version', ''), ('model', ' '), ('executed_at', 'ontem'), ('round', 0), ('origin', 'inventada')])
def test_rejeita_metadados_sem_rastreabilidade(tmp_path, field, value):
    invalid = metadata()
    invalid[field] = value
    with pytest.raises(ValueError):
        recorder().registrar_execucao(case(), 'Um fundamento.', invalid, tmp_path / 'invalid.json')
    assert not (tmp_path / 'invalid.json').exists()


def test_revisao_de_outra_saida_e_rejeitada(tmp_path):
    with pytest.raises(ValueError, match='hash'):
        recorder().registrar_execucao(case(), 'Outro fundamento.', metadata(), tmp_path / 'invalid.json', revisao=review())


def test_revisao_nao_pode_ser_reutilizada_apos_mudar_rubrica(tmp_path):
    original_review = review()
    original_review.pop('case_sha256')  # Contrato anterior não vinculava o caso.
    changed = case()
    changed['human_rubric'][0] = 'Outro critério jurídico que não foi revisado'
    with pytest.raises(ValueError):
        recorder().registrar_execucao(changed, 'Um fundamento.', metadata(), tmp_path / 'without-hash.json', revisao=original_review)


def test_revisao_com_hash_de_outro_caso_e_rejeitada(tmp_path):
    changed = case()
    changed['human_rubric'][0] = 'Critério alterado'
    with pytest.raises(ValueError, match='caso'):
        recorder().registrar_execucao(changed, 'Um fundamento.', metadata(), tmp_path / 'wrong-case.json', revisao=review())


def test_cli_exige_confirmacao_e_registra_catalogo_real(tmp_path, capsys):
    catalog = Path(__file__).resolve().parents[1] / 'evals/pedagogia/evals.json'
    case_id = json.loads(catalog.read_text(encoding='utf-8'))['evals'][0]['id']
    output = tmp_path / 'output.txt'
    output.write_text('Saída sintética para verificar apenas o registrador.', encoding='utf-8')
    meta = tmp_path / 'metadata.json'
    meta.write_text(json.dumps(metadata()), encoding='utf-8')
    target = tmp_path / 'record.json'
    args = ['--catalogo', str(catalog), '--caso', case_id, '--saida', str(output), '--metadados', str(meta), '--destino', str(target)]
    with pytest.raises(SystemExit) as stopped:
        recorder().main(args)
    assert stopped.value.code == 2
    assert not target.exists()
    assert recorder().main([*args, '--confirmar-gravacao-local']) in {0, 2}
    record = json.loads(target.read_text(encoding='utf-8'))
    assert record['case_snapshot']['id'] == case_id
    assert record['evaluation']['status'] != 'aprovado_com_revisao_humana'
    assert record['metadata']['origin'] == 'synthetic_fixture'
    assert 'run-teste-1' in capsys.readouterr().out
