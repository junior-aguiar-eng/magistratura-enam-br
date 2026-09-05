import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "evals" / "pedagogia" / "evals.json"
SCHEMA = ROOT / "evals" / "pedagogia" / "schema" / "evals.schema.json"
FRENTES = {
    "orquestracao",
    "dogmatica",
    "caso_complexo",
    "objetiva",
    "discursiva",
    "oral",
    "revisao",
    "curadoria",
    "planejamento",
    "comparacao",
    "perfil_local",
}


def carregar_json(caminho: Path):
    return json.loads(caminho.read_text(encoding="utf-8"))


def test_catalogo_pedagogico_inclui_baseline_conversacional_por_skill():
    assert CATALOGO.is_file(), "catálogo pedagógico ausente"
    casos = carregar_json(CATALOGO)["evals"]

    assert len(casos) == 44
    assert Counter(caso["skill"] for caso in casos) == {
        "estudar-direito-magistratura": 23,
        "curar-informativos-stf-stj": 6,
        "planejar-jurisprudencia": 5,
        "comparar-materiais-enam": 5,
        "acompanhar-percurso-magistratura": 5,
    }
    assert len({caso["id"] for caso in casos}) == 44


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


def test_casos_conversacionais_declaram_rota_transicao_e_fontes():
    catalogo = carregar_json(CATALOGO)
    casos = [caso for caso in catalogo["evals"] if caso["id"].startswith(("entrada-", "mudanca-", "fonte-", "negativo-"))]

    assert catalogo["baseline"] == "0.5.0"
    assert catalogo["target"] == "0.6.0"
    assert len(casos) == 18
    for caso in casos:
        assert caso["turns"]
        assert caso["expected_route"]
        assert caso["expected_transition"]
        assert caso["source_policy"]


def test_catalogo_cobre_todas_as_frentes_profissionalizadas():
    catalogo = carregar_json(CATALOGO)
    assert {caso["front"] for caso in catalogo["evals"] if "front" in caso} >= FRENTES
