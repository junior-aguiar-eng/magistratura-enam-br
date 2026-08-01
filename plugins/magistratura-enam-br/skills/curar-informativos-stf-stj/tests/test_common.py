import pytest
from common import (
    identificador_decisao,
    normalizar_processo,
    sanitizar_excel,
    validar_data_iso,
)


def test_normalizacao_equivale_formatos():
    assert normalizar_processo("REsp 1.340.553/RS") == normalizar_processo("REsp n. 1.340.553-RS")


@pytest.mark.parametrize("valor", ["=1+1", "+SUM(A1:A2)", "-2+3", "@cmd", "  =1+1"])
def test_sanitizacao_formula_excel(valor):
    assert sanitizar_excel(valor).startswith("'")


def test_identificador_distingue_decisoes_no_mesmo_processo():
    a = {"tribunal": "STJ", "processo": "REsp 1/RS", "data_julgamento": "2026-01-01", "tese_resumida": "A"}
    b = {"tribunal": "STJ", "processo": "REsp 1/RS", "data_julgamento": "2026-02-01", "tese_resumida": "B"}
    assert identificador_decisao(a) != identificador_decisao(b)


def test_data_invalida_rejeitada():
    with pytest.raises(ValueError):
        validar_data_iso("11/07/2026", "data")
