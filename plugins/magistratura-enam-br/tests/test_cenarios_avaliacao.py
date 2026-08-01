from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def texto(relativo: str) -> str:
    return (RAIZ / relativo).read_text(encoding="utf-8")


def test_cenarios_de_curadoria_preservam_limites_de_inferencia():
    cenarios = texto("skills/curar-informativos-stf-stj/references/cenarios-avaliacao.md")

    assert "## C1" in cenarios
    assert "## C2" in cenarios
    assert "rubrica depois da resposta" in cenarios
    assert "não o tratar como entendimento consolidado" in cenarios
    assert "superação apenas inferidos" in cenarios


def test_cenarios_de_questoes_preservam_tentativa_ativa():
    cenarios = texto("skills/estudar-direito-magistratura/references/cenarios-avaliacao.md")

    assert "## Q1" in cenarios
    assert "## Q2" in cenarios
    assert "rubrica depois da resposta" in cenarios
    assert "cinco alternativas funcionalmente comparáveis" in cenarios
    assert "antes da tentativa" in cenarios
