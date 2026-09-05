import json
from copy import deepcopy
from pathlib import Path

import pytest
import verificar_integracao as verificador
from jsonschema import Draft202012Validator


def carregar_json(caminho):
    return json.loads(caminho.read_text(encoding="utf-8"))


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("mode", "material", "external", "tiers"),
    [
        ("acervo_exclusivo", "disponivel", False, []),
        ("acervo_com_validacao_oficial", "disponivel", True, ["primaria"]),
        ("pesquisa_juridica_completa", "nao_aplicavel", True, ["primaria", "secundaria"]),
    ],
)
def test_tres_politicas_de_fontes_sao_validas(mode, material, external, tiers):
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "source-policy.schema.json")
    fixture = {
        "schema_version": "1.0.0",
        "mode": mode,
        "candidate_material": material,
        "allow_external_research": external,
        "allowed_source_tiers": tiers,
        "registry_version": "1.0.0",
    }

    Draft202012Validator(schema).validate(fixture)


def test_acervo_exclusivo_nao_admite_pesquisa_externa():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "source-policy.schema.json")
    fixture = {
        "schema_version": "1.0.0",
        "mode": "acervo_exclusivo",
        "candidate_material": "disponivel",
        "allow_external_research": True,
        "allowed_source_tiers": ["primaria"],
        "registry_version": "1.0.0",
    }

    assert not Draft202012Validator(schema).is_valid(fixture)


def test_registro_fechado_atende_schema_e_hierarquia():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "trusted-source-registry.schema.json")
    registro = carregar_json(PLUGIN_ROOT / "references" / "fontes-confiaveis.json")
    Draft202012Validator(schema).validate(registro)

    assert {item["id"] for item in registro["sources"]} == verificador.FONTES_CONFIAVEIS
    assert all(item.get("authoritative_for") for item in registro["sources"] if item["tier"] == "primaria")
    assert all(item.get("limitations") for item in registro["sources"] if item["tier"] == "secundaria")


def test_dominio_e_comparado_por_hostname_exato():
    dominios = {"www.stf.jus.br"}

    assert verificador.dominio_registrado("https://www.stf.jus.br/portal/", dominios)
    assert not verificador.dominio_registrado("https://www.stf.jus.br.evil.example/", dominios)
    assert not verificador.dominio_registrado("https://evil.example/?url=www.stf.jus.br", dominios)


def test_registro_rejeita_secundaria_sem_limitacoes():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "trusted-source-registry.schema.json")
    registro = carregar_json(PLUGIN_ROOT / "references" / "fontes-confiaveis.json")
    invalido = deepcopy(registro)
    secundaria = next(item for item in invalido["sources"] if item["tier"] == "secundaria")
    del secundaria["limitations"]

    assert not Draft202012Validator(schema).is_valid(invalido)
