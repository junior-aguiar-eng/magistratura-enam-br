import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    path = ROOT / "scripts" / "referencias_pedagogicas.py"
    spec = importlib.util.spec_from_file_location("referencias_pedagogicas", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _schema(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_precedente_e_delta_preservam_identificador_e_fontes():
    referencias = _load_module()
    precedente = referencias.content_ref_from_precedente(
        {
            "id_decisao": "STJ-REsp-123",
            "disciplina": "Direito Civil",
            "tema": "Responsabilidade civil",
            "fontes_essenciais": ["https://processo.stj.jus.br/123"],
            "estado_jurisprudencial": "confirmado",
        },
        subtema="Dano moral",
    )
    delta = referencias.content_ref_from_delta(
        {
            "id_item": "delta-2026-01",
            "disciplina": "Direito Civil",
            "tema_subtema": "Responsabilidade civil / Dano moral",
            "referencias_atuais": [
                {"documento": "Apostila 2026", "pagina": "42", "localizacao": "item 3"}
            ],
        }
    )

    assert precedente["id"] == "STJ-REsp-123"
    assert precedente["source_refs"] == ["https://processo.stj.jus.br/123"]
    assert delta["id"] == "delta-2026-01"
    assert delta["source_refs"] == ["Apostila 2026 | p. 42 | item 3"]


def test_schemas_aceitam_content_ref_novo_e_legado_sem_content_ref():
    content_ref = {
        "kind": "precedente",
        "id": "STF-Tema-123",
        "disciplina": "Direito Constitucional",
        "tema": "Direitos fundamentais",
        "subtema": "Liberdade de expressão",
        "source_refs": ["https://portal.stf.jus.br/tema123"],
        "source_state": "confirmado",
    }
    precedente_schema = _schema("skills/curar-informativos-stf-stj/modelos/precedentes.schema.json")
    comparativo_schema = _schema("skills/comparar-materiais-enam/modelos/comparativo.schema.json")

    precedente = {
        "processo": "RE 123",
        "tribunal": "STF",
        "estado_jurisprudencial": "confirmado",
        "grau_confianca": "alto",
        "content_ref": content_ref,
    }
    legado = {k: v for k, v in precedente.items() if k != "content_ref"}
    Draft202012Validator(precedente_schema).validate([precedente])
    Draft202012Validator(precedente_schema).validate([legado])

    item = {
        "id_item": "delta-1",
        "disciplina": "Direito Constitucional",
        "tema_subtema": "Direitos fundamentais / Liberdade de expressão",
        "referencias_anteriores": [],
        "referencias_atuais": [],
        "tipo_correspondencia": "CORRESPONDENCIA TEMATICA CONFIRMADA",
        "classificacao": "SEM DELTA",
        "delta_real": "Sem alteração material.",
        "acao_recomendada": "SEM_ACAO",
        "evidencias": [{"documento": "A", "pagina": "1", "localizacao": "item 1"}],
        "content_ref": {
            **content_ref,
            "kind": "delta_documental",
            "id": "delta-1",
            "source_state": "documental_confirmado",
        },
    }
    legado_item = {k: v for k, v in item.items() if k != "content_ref"}
    Draft202012Validator(comparativo_schema).validate(
        {"id_execucao": "exec-1", "escopo": "teste", "itens": [item, legado_item]}
    )


def test_delta_documental_nao_produz_avaliacao_do_candidato():
    referencias = _load_module()
    content_ref = referencias.content_ref_from_delta(
        {
            "id_item": "delta-1",
            "disciplina": "Direito Penal",
            "tema_subtema": "Tipicidade / Erro de tipo",
            "referencias_atuais": [],
        }
    )
    assert not ({"candidate_error", "mastery", "performance"} & content_ref.keys())
