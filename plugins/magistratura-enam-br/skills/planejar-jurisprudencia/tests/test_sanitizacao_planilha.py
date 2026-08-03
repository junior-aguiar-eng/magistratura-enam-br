import pytest
from sanitizacao_planilha import sanitizar_excel


@pytest.mark.parametrize("valor", ["=1+1", "+SUM(A1:A2)", "-2+3", "@cmd", "  =1+1"])
def test_sanitizacao_formula_excel(valor):
    assert sanitizar_excel(valor).startswith("'")


def test_sanitizacao_preserva_texto_comum():
    assert sanitizar_excel("  Tema de controle  ") == "Tema de controle"


def test_sanitizacao_converte_none_em_texto_vazio():
    assert sanitizar_excel(None) == ""
