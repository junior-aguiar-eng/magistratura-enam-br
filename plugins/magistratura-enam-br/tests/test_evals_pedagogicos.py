import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "evals" / "pedagogia" / "evals.json"
SCHEMA = ROOT / "evals" / "pedagogia" / "schema" / "evals.schema.json"


def carregar_json(caminho: Path):
    return json.loads(caminho.read_text(encoding="utf-8"))


def test_catalogo_pedagogico_tem_dezesseis_casos_distribuidos_por_skill():
    assert CATALOGO.is_file(), "catálogo pedagógico ausente"
    casos = carregar_json(CATALOGO)["evals"]

    assert len(casos) == 16
    assert Counter(caso["skill"] for caso in casos) == {
        "estudar-direito-magistratura": 5,
        "curar-informativos-stf-stj": 3,
        "planejar-jurisprudencia": 4,
        "comparar-materiais-enam": 2,
        "acompanhar-percurso-magistratura": 2,
    }
    assert len({caso["id"] for caso in casos}) == 16


def test_catalogo_e_casos_invalidos_sao_avaliados_pelo_schema():
    assert SCHEMA.is_file(), "schema das avaliações ausente"
    assert CATALOGO.is_file(), "catálogo pedagógico ausente"
    schema = carregar_json(SCHEMA)
    catalogo = carregar_json(CATALOGO)
    validator = Draft202012Validator(schema)

    assert list(validator.iter_errors(catalogo)) == []

    caso_invalido = json.loads(json.dumps(catalogo, ensure_ascii=False))
    del caso_invalido["evals"][0]["human_rubric"]
    assert list(validator.iter_errors(caso_invalido))


def test_todo_caso_tem_resultado_esperado_rubrica_humana_e_risco():
    assert CATALOGO.is_file(), "catálogo pedagógico ausente"
    casos = carregar_json(CATALOGO)["evals"]

    for caso in casos:
        assert caso["expected_output"].strip()
        assert caso["human_rubric"]
        assert caso["risk_tags"]
        assert any(item["kind"] == "human" for item in caso["assertions"])
