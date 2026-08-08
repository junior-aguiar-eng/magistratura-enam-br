import pytest
from sanitizacao_planilha import sanitizar_excel


@pytest.mark.parametrize("valor", ["=1+1", "+SUM(A1:A2)", "-2+3", "@cmd", "  =1+1"])
def test_sanitizacao_formula_excel(valor):
    resultado = sanitizar_excel(valor)

    assert resultado == "'" + valor
    assert resultado[0] == "'"


@pytest.mark.parametrize("valor", ["\t=1+1", "\n@cmd", "   -2+3"])
def test_sanitizacao_desarma_formula_oculta_por_whitespace(valor):
    assert sanitizar_excel(valor) == "'" + valor


def test_sanitizacao_preserva_texto_comum():
    assert sanitizar_excel("  Tema de controle  ") == "Tema de controle"


def test_sanitizacao_converte_none_em_texto_vazio():
    assert sanitizar_excel(None) == ""
