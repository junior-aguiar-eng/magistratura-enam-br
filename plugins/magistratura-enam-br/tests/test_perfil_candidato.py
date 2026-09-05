import json
from copy import deepcopy

import perfil_candidato as perfil
import pytest
from test_eventos_aprendizagem import criar_evento
from test_schemas_pedagogicos import criar_evento_v2


def evento(event_id, ocorrido, modalidade="questao_objetiva", resultado="parcial"):
    item = criar_evento(event_id, resultado)
    item["occurred_at"] = ocorrido
    item["activity"]["modality"] = modalidade
    return item


def test_reconstrucao_e_deterministica_com_eventos_fora_de_ordem():
    anterior = evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")
    posterior = evento(
        "evt_11a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-04T12:00:00Z", resultado="correto"
    )

    assert perfil.reconstruir_perfil([posterior, anterior]) == perfil.reconstruir_perfil([anterior, posterior])


def test_reconstrucao_rejeita_evento_duplicado():
    item = evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")

    with pytest.raises(ValueError, match="duplicado"):
        perfil.reconstruir_perfil([item, item])


def test_competencias_sao_independentes_por_modalidade_e_preservam_historico():
    objetiva = evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")
    oral = evento(
        "evt_11a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-04T12:00:00Z", "prova_oral", "correto"
    )
    perfil_reconstruido = perfil.reconstruir_perfil([objetiva, oral])

    assert [item["competency_id"] for item in perfil_reconstruido["competencies"]] == [
        "prescricao-decadencia--prova-oral",
        "prescricao-decadencia--questao-objetiva",
    ]
    assert sum(len(item["observations"]) for item in perfil_reconstruido["competencies"]) == 2


def test_remediacao_abre_com_erro_e_fecha_com_acerto_posterior():
    erro = evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")
    acerto = evento(
        "evt_11a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-04T12:00:00Z", resultado="correto"
    )

    assert len(perfil.reconstruir_perfil([erro])["open_remediations"]) == 1
    assert perfil.reconstruir_perfil([erro, acerto])["open_remediations"] == []


def test_salvar_atomico_permite_apagar_e_reconstruir_sem_delta(tmp_path):
    eventos = [evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")]
    esperado = perfil.reconstruir_perfil(eventos)
    caminho = tmp_path / "perfil.json"

    perfil.salvar_perfil_atomico(caminho, esperado)
    caminho.unlink()
    perfil.salvar_perfil_atomico(caminho, perfil.reconstruir_perfil(eventos))

    assert json.loads(caminho.read_text(encoding="utf-8")) == esperado


def test_perfil_v2_separa_preferencias_explicitas_de_inferencias():
    configuracao = {
        "schema_version": "1.0.0",
        "objectives": ["Magistratura estadual"],
        "preferences": {"feedback_mode": "adaptativo", "preferred_modalities": ["questao_objetiva"]},
    }
    reconstruido = perfil.reconstruir_perfil([], configuracao)
    assert reconstruido["schema_version"] == "2.0.0"
    assert reconstruido["declared"] == configuracao
    assert reconstruido["competencies"] == []


def test_perfil_sem_configuracao_nao_inventa_preferencia():
    reconstruido = perfil.reconstruir_perfil([])
    assert reconstruido["declared"] == {"schema_version": "1.0.0", "objectives": [], "preferences": {}}


def test_acerto_assistido_nao_demonstra_transferencia_autonoma():
    item = criar_evento_v2()
    item["activity"]["assistance_level"] = "conducao_completa"
    competencia = perfil.reconstruir_perfil([item])["competencies"][0]
    assert competencia["evidence"]["aplicacao_fatos_novos"] == "em_desenvolvimento"


def test_chave_de_competencia_aceita_content_ref_novo_e_legado():
    legado = evento("evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", "2026-09-03T12:00:00Z")
    novo = deepcopy(criar_evento_v2())
    assert len(perfil.reconstruir_perfil([legado, novo])["competencies"]) == 2
