def test_estudo_distingue_contextos_sem_impor_template(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    for contexto in ("resposta pontual", "sessão aprofundada", "revisão", "síntese"):
        assert contexto in referencia
    assert "não são seções obrigatórias" in referencia


def test_norma_e_jurisprudencia_entram_na_construcao_dogmatica(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    for funcao in ("institui", "delimita", "excepciona", "define", "restringe", "atualiza", "aplica"):
        assert funcao in referencia
    assert "fontes jurisprudenciais oficiais" in referencia
    assert "base consultada" in referencia
    assert "desfile de artigos" in referencia


def test_sessao_e_cumulativa_sem_despejo_editorial(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    assert "unidade intelectualmente completa" in referencia
    assert "prepara o núcleo seguinte" in referencia
    assert "não reinicie" in referencia
    assert "glossário" in referencia
