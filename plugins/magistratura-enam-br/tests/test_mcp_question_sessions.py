import copy
import json
from pathlib import Path

import pytest

from mcp_server.questions import QuestionConflictError, QuestionRepository


def sessao(state: str = "ready") -> dict:
    return {
        "schema_version": "1.0.0",
        "projection": "private",
        "session_id": "qsn_0123456789abcdef",
        "state": state,
        "created_at": "2026-09-05T18:00:00Z",
        "subject": "Direito Civil",
        "topic": "Obrigações",
        "mode": "training",
        "prompt": "Assinale a alternativa correta.",
        "alternatives": [
            {"id": letra, "text": f"Alternativa {letra}"}
            for letra in ("A", "B", "C", "D", "E")
        ],
        "correct_option": "C",
        "correction": {
            "correct_rationale": "A alternativa C aplica corretamente a regra.",
            "distractor_analysis": [
                {"option": letra, "analysis": f"Erro jurídico da alternativa {letra}."}
                for letra in ("A", "B", "D", "E")
            ],
            "exceptions": ["Exceção juridicamente relevante."],
            "traps": ["Confusão entre regra e exceção."],
        },
        "sources": [
            {
                "source_id": "src_cc_1",
                "kind": "planalto",
                "title": "Código Civil",
                "url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",
                "accessed_at": "2026-09-05T18:00:00Z",
                "role": "regra",
                "excerpt": "Art. 189.",
            }
        ],
        "source_status": "verified",
    }


def repositorio(tmp_path: Path) -> QuestionRepository:
    state_dir = tmp_path / ".estudo-juridico"
    state_dir.mkdir()
    return QuestionRepository(state_dir)


def test_criacao_persiste_privado_e_retorna_somente_projecao_publica(tmp_path):
    repo = repositorio(tmp_path)

    publica = repo.create_session(sessao())

    assert publica["projection"] == "public"
    assert publica["state"] == "ready"
    assert "correct_option" not in publica
    assert "correction" not in publica
    persistida = json.loads(repo.questions_path.read_text(encoding="utf-8"))
    assert persistida["correct_option"] == "C"


def test_fluxo_draft_ready_answered_e_recarregavel(tmp_path):
    repo = repositorio(tmp_path)
    repo.create_draft(sessao("draft"))
    publica = repo.mark_ready("qsn_0123456789abcdef")

    corrigida = repo.answer(
        "qsn_0123456789abcdef", "B", answered_at="2026-09-05T18:05:00Z"
    )
    recarregado = QuestionRepository(repo.state_dir).get_session("qsn_0123456789abcdef")

    assert publica["state"] == "ready"
    assert corrigida["projection"] == "corrected"
    assert corrigida["state"] == "answered"
    assert corrigida["result"] == "incorrect"
    assert corrigida["correct_option"] == "C"
    assert recarregado["state"] == "answered"


def test_resposta_repetida_e_idempotente_e_alternativa_divergente_conflita(tmp_path):
    repo = repositorio(tmp_path)
    repo.create_session(sessao())

    primeira = repo.answer(
        "qsn_0123456789abcdef", "C", answered_at="2026-09-05T18:05:00Z"
    )
    repetida = repo.answer(
        "qsn_0123456789abcdef", "C", answered_at="2026-09-05T18:06:00Z"
    )

    assert repetida == primeira
    assert len(repo.attempts_store.read_all()) == 1
    with pytest.raises(QuestionConflictError, match="já respondida"):
        repo.answer("qsn_0123456789abcdef", "A", answered_at="2026-09-05T18:07:00Z")


def test_invalidacao_explicita_impede_transicao_regressiva(tmp_path):
    repo = repositorio(tmp_path)
    repo.create_session(sessao())

    invalidada = repo.invalidate(
        "qsn_0123456789abcdef",
        reason="Questão sem chave única após auditoria.",
        invalidated_at="2026-09-05T18:03:00Z",
    )

    assert invalidada["state"] == "invalidated"
    with pytest.raises(QuestionConflictError, match="invalidada"):
        repo.mark_ready("qsn_0123456789abcdef")
    with pytest.raises(QuestionConflictError, match="invalidada"):
        repo.answer("qsn_0123456789abcdef", "C", answered_at="2026-09-05T18:05:00Z")


def test_tentativa_gera_evento_pedagogico_compativel_sem_perfil_paralelo(tmp_path):
    repo = repositorio(tmp_path)
    repo.create_session(sessao())

    repo.answer("qsn_0123456789abcdef", "B", answered_at="2026-09-05T18:05:00Z")

    eventos = repo.learning_events_store.read_all()
    assert len(eventos) == 1
    assert eventos[0]["activity"]["modality"] == "questao_objetiva"
    assert eventos[0]["performance"]["result"] == "incorreto"
    assert not (repo.state_dir / "perfil-mcp.json").exists()


def test_payload_privado_invalido_nao_e_persistido(tmp_path):
    repo = repositorio(tmp_path)
    invalida = copy.deepcopy(sessao())
    invalida["alternatives"].pop()

    with pytest.raises(ValueError, match="Registro inválido"):
        repo.create_session(invalida)

    assert not repo.questions_path.exists()
