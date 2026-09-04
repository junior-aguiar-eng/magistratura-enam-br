import json

import eventos_aprendizagem as eventos
import pytest


def criar_evento(event_id="evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc", resultado="parcial"):
    return {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "occurred_at": "2026-09-04T12:00:00Z",
        "skill": "estudar-direito-magistratura",
        "content_ref": {"content_id": "prescricao-decadencia", "source_type": "fonte_oficial"},
        "activity": {"modality": "questao_objetiva", "attempt_observed": True},
        "performance": {
            "result": resultado,
            "error_types": [] if resultado == "correto" else ["distincao"],
            "domain_evidence": ["evocacao_regra"],
            "confidence": "media",
        },
        "routing": {"target_skill": "estudar-direito-magistratura", "reason_codes": []},
    }


def test_validar_evento_aceita_valido_e_rejeita_schema_invalido():
    assert eventos.validar_evento(criar_evento()) == []
    invalido = criar_evento()
    invalido["performance"]["result"] = "quase"

    assert eventos.validar_evento(invalido)


def test_append_e_leitura_preservam_uma_linha_utf8_por_evento(tmp_path):
    log = tmp_path / "eventos.jsonl"
    evento = criar_evento()

    eventos.acrescentar_evento(log, evento)

    assert eventos.ler_eventos(log) == [evento]
    assert len(log.read_text(encoding="utf-8").splitlines()) == 1


def test_evento_invalido_ou_duplicado_nao_altera_log(tmp_path):
    log = tmp_path / "eventos.jsonl"
    evento = criar_evento()
    eventos.acrescentar_evento(log, evento)
    original = log.read_bytes()

    with pytest.raises(ValueError, match="duplicado"):
        eventos.acrescentar_evento(log, evento)
    with pytest.raises(ValueError, match="inválido"):
        eventos.acrescentar_evento(log, {"event_id": "invalido"})

    assert log.read_bytes() == original


def test_linha_corrompida_impede_leitura_e_append_sem_alteracao(tmp_path):
    log = tmp_path / "eventos.jsonl"
    log.write_text(json.dumps(criar_evento()) + "\n{\n", encoding="utf-8")
    original = log.read_bytes()

    with pytest.raises(ValueError, match="linha 2"):
        eventos.ler_eventos(log)
    with pytest.raises(ValueError, match="linha 2"):
        eventos.acrescentar_evento(log, criar_evento("evt_11a06d61-62eb-71f1-b7c0-5e19a67c47dc"))

    assert log.read_bytes() == original


def test_nao_cria_diretorio_pai_sem_opcao_explicita(tmp_path):
    log = tmp_path / "ausente" / "eventos.jsonl"

    with pytest.raises(FileNotFoundError):
        eventos.acrescentar_evento(log, criar_evento())
    eventos.acrescentar_evento(log, criar_evento(), criar_diretorio=True)

    assert log.is_file()

