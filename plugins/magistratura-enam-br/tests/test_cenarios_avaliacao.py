def test_cenarios_de_curadoria_preservam_limites_de_inferencia(texto):
    cenarios = texto("skills/curar-informativos-stf-stj/references/cenarios-avaliacao.md")

    assert "## C1" in cenarios
    assert "## C2" in cenarios
    assert "rubrica depois da resposta" in cenarios
    assert "não o tratar como entendimento consolidado" in cenarios
    assert "superação apenas inferidos" in cenarios


def test_cenarios_de_questoes_preservam_tentativa_ativa(texto):
    cenarios = texto("skills/estudar-direito-magistratura/references/cenarios-avaliacao.md")

    assert "## Q1" in cenarios
    assert "## Q2" in cenarios
    assert "## Q3" in cenarios
    assert "## Q4" in cenarios
    assert "## Q5" in cenarios
    assert "rubrica depois da resposta" in cenarios
    assert "cinco alternativas funcionalmente comparáveis" in cenarios
    assert "antes da tentativa" in cenarios
    assert "regra–fato–consequência" in cenarios
    assert "alternativas simétricas" in cenarios
    assert "Insumo introdutório insuficiente" in cenarios
