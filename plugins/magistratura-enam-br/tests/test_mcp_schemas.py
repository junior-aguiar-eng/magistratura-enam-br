import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "mcp_server" / "schemas"


def carregar_schema(nome: str) -> dict:
    return json.loads((SCHEMAS / nome).read_text(encoding="utf-8"))


def validar(nome: str, instancia: dict) -> None:
    schema = carregar_schema(nome)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instancia)


def test_sdk_mcp_v2_esta_disponivel():
    from mcp.server import MCPServer

    assert MCPServer is not None


@pytest.fixture
def referencias() -> list[dict]:
    return [
        {
            "source_id": "src_cc_1",
            "kind": "planalto",
            "title": "Código Civil",
            "url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",
            "accessed_at": "2026-09-05T18:00:00Z",
            "role": "regra",
            "excerpt": "Art. 189.",
        }
    ]


@pytest.fixture
def alternativas() -> list[dict]:
    return [
        {"id": letra, "text": f"Alternativa {letra}"}
        for letra in ("A", "B", "C", "D", "E")
    ]


@pytest.fixture
def correcao() -> dict:
    return {
        "correct_rationale": "A alternativa C aplica corretamente a regra.",
        "distractor_analysis": [
            {"option": letra, "analysis": f"Erro jurídico da alternativa {letra}."}
            for letra in ("A", "B", "D", "E")
        ],
        "exceptions": ["A conclusão muda se o pressuposto fático não estiver presente."],
        "traps": ["Confusão entre regra e exceção."],
    }


def test_quatro_schemas_sao_draft_2020_12_validos():
    nomes = {
        "library-config.schema.json",
        "indexed-document.schema.json",
        "question-session.schema.json",
        "question-attempt.schema.json",
    }
    assert {item.name for item in SCHEMAS.glob("*.schema.json")} == nomes
    for nome in nomes:
        schema = carregar_schema(nome)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        Draft202012Validator.check_schema(schema)


def test_configuracao_e_documento_indexado_minimos_sao_validos():
    validar(
        "library-config.schema.json",
        {
            "schema_version": "1.0.0",
            "library_root": "C:\\Estudo\\Biblioteca",
            "write_consent": True,
            "excluded_directories": [".git", ".estudo-juridico", "node_modules"],
            "limits": {"max_file_bytes": 2000000, "max_result_chunks": 12},
        },
    )
    validar(
        "indexed-document.schema.json",
        {
            "schema_version": "1.0.0",
            "document_id": "doc_0123456789abcdef",
            "relative_path": "civil/obrigacoes.md",
            "size_bytes": 2048,
            "modified_at": "2026-09-05T18:00:00Z",
            "sha256": "a" * 64,
            "title": "Obrigações",
            "chunks": [
                {
                    "chunk_id": "chk_0123456789abcdef",
                    "heading": "Inadimplemento",
                    "ordinal": 0,
                    "text": "Conteúdo jurídico indexado.",
                }
            ],
        },
    )


def test_sessao_privada_com_cinco_alternativas_e_correcao_completa_e_valida(
    alternativas, correcao, referencias
):
    validar(
        "question-session.schema.json",
        {
            "schema_version": "1.0.0",
            "projection": "private",
            "session_id": "qsn_0123456789abcdef",
            "state": "ready",
            "created_at": "2026-09-05T18:00:00Z",
            "subject": "Direito Civil",
            "topic": "Obrigações",
            "mode": "training",
            "prompt": "Assinale a alternativa correta.",
            "alternatives": alternativas,
            "correct_option": "C",
            "correction": correcao,
            "sources": referencias,
            "source_status": "verified",
        },
    )


@pytest.mark.parametrize("quantidade", [4, 6])
def test_sessao_rejeita_quantidade_diferente_de_cinco_alternativas(
    quantidade, alternativas, correcao, referencias
):
    sessao = {
        "schema_version": "1.0.0",
        "projection": "private",
        "session_id": "qsn_0123456789abcdef",
        "state": "ready",
        "created_at": "2026-09-05T18:00:00Z",
        "subject": "Direito Civil",
        "topic": "Obrigações",
        "mode": "training",
        "prompt": "Assinale a alternativa correta.",
        "alternatives": alternativas[:quantidade]
        if quantidade == 4
        else alternatives_with_extra(alternativas),
        "correct_option": "C",
        "correction": correcao,
        "sources": referencias,
        "source_status": "verified",
    }
    with pytest.raises(ValidationError):
        validar("question-session.schema.json", sessao)


def alternatives_with_extra(alternativas: list[dict]) -> list[dict]:
    return [*alternativas, {"id": "F", "text": "Alternativa F"}]


def test_projecao_publica_rejeita_gabarito_e_correcao(alternativas, referencias):
    publica = {
        "schema_version": "1.0.0",
        "projection": "public",
        "session_id": "qsn_0123456789abcdef",
        "state": "ready",
        "created_at": "2026-09-05T18:00:00Z",
        "subject": "Direito Civil",
        "topic": "Obrigações",
        "mode": "training",
        "prompt": "Assinale a alternativa correta.",
        "alternatives": alternativas,
        "sources": referencias,
        "source_status": "caution",
        "caution_notice": "A atualidade das fontes externas não foi confirmada.",
    }
    validar("question-session.schema.json", publica)

    vazamento = copy.deepcopy(publica)
    vazamento["correct_option"] = "C"
    with pytest.raises(ValidationError):
        validar("question-session.schema.json", vazamento)


def test_sessao_caution_exige_aviso_explicito(alternativas, referencias):
    publica = {
        "schema_version": "1.0.0",
        "projection": "public",
        "session_id": "qsn_0123456789abcdef",
        "state": "ready",
        "created_at": "2026-09-05T18:00:00Z",
        "subject": "Direito Civil",
        "topic": "Obrigações",
        "mode": "training",
        "prompt": "Assinale a alternativa correta.",
        "alternatives": alternativas,
        "sources": referencias,
        "source_status": "caution",
    }
    with pytest.raises(ValidationError):
        validar("question-session.schema.json", publica)


def test_tentativa_corrigida_vincula_questao_fontes_e_gabarito(referencias):
    validar(
        "question-attempt.schema.json",
        {
            "schema_version": "1.0.0",
            "attempt_id": "qat_0123456789abcdef",
            "session_id": "qsn_0123456789abcdef",
            "question_hash": "b" * 64,
            "answered_at": "2026-09-05T18:05:00Z",
            "selected_option": "B",
            "correct_option": "C",
            "result": "incorrect",
            "source_refs": [item["source_id"] for item in referencias],
        },
    )
