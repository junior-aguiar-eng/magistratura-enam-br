import copy
import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

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

    assert len(casos) >= 44
    contagem = Counter(caso["skill"] for caso in casos)
    for skill, minimo in {
        "estudar-direito-magistratura": 23,
        "curar-informativos-stf-stj": 6,
        "planejar-jurisprudencia": 5,
        "comparar-materiais-enam": 5,
        "acompanhar-percurso-magistratura": 5,
    }.items():
        assert contagem[skill] >= minimo
    assert len({caso["id"] for caso in casos}) == len(casos)


def test_catalogo_e_casos_invalidos_sao_avaliados_pelo_schema():
    assert SCHEMA.is_file(), "schema das avaliações ausente"
    assert CATALOGO.is_file(), "catálogo pedagógico ausente"
    schema = carregar_json(SCHEMA)
    catalogo = carregar_json(CATALOGO)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

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
    assert len(casos) >= 18
    for caso in casos:
        assert caso["turns"]
        assert caso["expected_route"]
        assert caso["expected_transition"]
        assert caso["source_policy"]


def test_catalogo_cobre_todas_as_frentes_profissionalizadas():
    catalogo = carregar_json(CATALOGO)
    assert {caso["front"] for caso in catalogo["evals"] if "front" in caso} >= FRENTES


def test_casos_fgv_separam_invocacao_explicita_pedido_generico_e_skill_ausente():
    casos = {caso["id"]: caso for caso in carregar_json(CATALOGO)["evals"]}
    explicito = casos["externo-fgv-explicito-disponivel"]
    generico = casos["entrada-fgv-generica-plugin"]
    ausente = casos["entrada-fgv-externa-indisponivel"]

    assert explicito["expected_external_skill"] == "treinador-fgv-magistratura"
    assert "expected_route" not in explicito
    assert explicito["expected_transition"] == "continuidade_direta"
    assert generico["expected_route"] == "estudar-direito-magistratura"
    assert generico["expected_transition"] == "continuidade_direta"
    assert ausente["expected_route"] == "acompanhar-percurso-magistratura"
    assert ausente["expected_transition"] == "bloqueio_por_insumo"
    assert all(
        caso["source_policy"] == "nao_aplicavel"
        and any(assertion["kind"] == "human" for assertion in caso["assertions"])
        for caso in (explicito, generico, ausente)
    )

    validator = Draft202012Validator(carregar_json(SCHEMA), format_checker=FormatChecker())
    catalogo = carregar_json(CATALOGO)
    externo_com_rota_interna = copy.deepcopy(catalogo)
    next(
        caso for caso in externo_com_rota_interna["evals"] if caso["id"] == explicito["id"]
    )["expected_route"] = "estudar-direito-magistratura"
    assert list(validator.iter_errors(externo_com_rota_interna))

    interno_com_destino_externo = copy.deepcopy(catalogo)
    next(
        caso for caso in interno_com_destino_externo["evals"] if caso["id"] == generico["id"]
    )["expected_external_skill"] = "treinador-fgv-magistratura"
    assert list(validator.iter_errors(interno_com_destino_externo))


def test_schema_aceita_fundamentacao_juridica_e_rejeita_metadados_incompletos():
    validator = Draft202012Validator(carregar_json(SCHEMA), format_checker=FormatChecker())
    catalogo = carregar_json(CATALOGO)
    caso = catalogo["evals"][0]
    caso["legal_grounding"] = {
        "checked_at": "2026-09-23",
        "cutoff_date": "2026-09-23",
        "claims": [{
            "id": "pretensao",
            "expected_conclusion": "A violação faz nascer a pretensão.",
            "official_source": "src_cc-2002-compilado",
            "locator": "Art. 189",
            "supports": "O dispositivo relaciona violação e pretensão.",
        }],
        "human_review": {"review_status": "pending", "review_note": ""},
    }
    assert list(validator.iter_errors(catalogo)) == []

    invalidos = []
    for alteracao in (
        lambda base: base.update(checked_at="2026-13-40"),
        lambda base: base["claims"][0].pop("official_source"),
        lambda base: base["human_review"].update(review_status="approved", review_note=""),
        lambda base: base["human_review"].update(review_status="approved", review_note="   "),
        lambda base: base.update(claims=[], human_review={"review_status": "approved", "review_note": "Revisto."}),
    ):
        invalido = copy.deepcopy(catalogo)
        alteracao(invalido["evals"][0]["legal_grounding"])
        invalidos.append(invalido)
    assert all(list(validator.iter_errors(invalido)) for invalido in invalidos)


def _referencias_de_fontes_validas(catalogo: dict, ids_fontes: set[str]) -> bool:
    return all(
        claim["official_source"] in ids_fontes
        for caso in catalogo["evals"]
        for claim in caso.get("legal_grounding", {}).get("claims", [])
    )


def test_benchmark_piloto_usa_fontes_oficiais_localizaveis_e_revisao_pendente():
    fontes = carregar_json(ROOT / "evals" / "pedagogia" / "benchmark-juridico" / "fontes.json")
    ids_fontes = {fonte["id"] for fonte in fontes["sources"]}
    assert ids_fontes
    assert all(fonte["url"].startswith("https://www.planalto.gov.br/") for fonte in fontes["sources"])

    catalogo = carregar_json(CATALOGO)
    casos = [caso for caso in catalogo["evals"] if caso["id"].startswith("juridico-")]
    assert len(casos) >= 8
    assert {caso["front"] for caso in casos} >= {
        "dogmatica", "caso_complexo", "objetiva", "discursiva", "oral", "revisao"
    }
    for caso in casos:
        base = caso["legal_grounding"]
        assert base["human_review"]["review_status"] == "pending"
        assert base["claims"]
    assert _referencias_de_fontes_validas(catalogo, ids_fontes)

    caso_sem_fonte = copy.deepcopy(catalogo)
    caso_sem_fonte["evals"][0]["legal_grounding"] = copy.deepcopy(casos[0]["legal_grounding"])
    caso_sem_fonte["evals"][0]["legal_grounding"]["claims"][0]["official_source"] = "src_inexistente"
    assert not _referencias_de_fontes_validas(caso_sem_fonte, ids_fontes)
