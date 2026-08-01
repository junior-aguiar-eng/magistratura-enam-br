import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


def schema(nome):
    return json.loads((ROOT / "modelos" / nome).read_text(encoding="utf-8"))


def validar(nome, instancia):
    Draft202012Validator(schema(nome), format_checker=FormatChecker()).validate(instancia)


def boletim():
    return {
        "titulo_boletim": "Boletim",
        "data_geracao": "2026-07-11",
        "nota_metodologica": "Método.",
        "julgados_stf": [{
            "titulo": "Tema", "comentario": "Comentário", "estado_jurisprudencial": "confirmado",
            "grau_confianca": "alto", "data_verificacao": "2026-07-11", "fontes_essenciais": []
        }],
        "julgados_stj": []
    }


def test_schema_boletim_valido():
    validar("boletim.schema.json", boletim())


def test_schema_boletim_exige_nota_quando_controvertido():
    d = boletim(); d["julgados_stf"][0]["estado_jurisprudencial"] = "controvertido"
    with pytest.raises(ValidationError):
        validar("boletim.schema.json", d)


def test_schema_boletim_rejeita_data_invalida():
    d = boletim(); d["data_geracao"] = "11/07/2026"
    with pytest.raises(ValidationError):
        validar("boletim.schema.json", d)


def test_schema_precedente_valido():
    validar("precedentes.schema.json", [{
        "processo": "RE 1/DF", "tribunal": "STF", "estado_jurisprudencial": "confirmado", "grau_confianca": "alto"
    }])


def test_schema_precedente_confirmado_aceita_nota_vazia():
    validar("precedentes.schema.json", [{
        "processo": "RE 1/DF", "tribunal": "STF", "estado_jurisprudencial": "confirmado",
        "grau_confianca": "alto", "nota_estado": ""
    }])


def test_schema_precedente_rejeita_tribunal():
    with pytest.raises(ValidationError):
        validar("precedentes.schema.json", [{
            "processo": "RE 1", "tribunal": "TRF", "estado_jurisprudencial": "confirmado", "grau_confianca": "alto"
        }])
