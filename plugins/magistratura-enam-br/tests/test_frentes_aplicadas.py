def test_objetiva_distingue_treino_simulado_e_remediacao(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md").casefold()
    for modo in ("treino", "simulado", "remediação"):
        assert modo in referencia
    assert "hipótese independente" in referencia


def test_discursiva_distingue_indispensavel_excelencia_e_acessorio(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/discursivas.md").casefold()
    for criterio in ("atendimento ao comando", "aplicação aos fatos", "objeções", "economia argumentativa"):
        assert criterio in referencia
    for faixa in ("indispensável", "excelência", "acessório"):
        assert faixa in referencia


def test_oral_usa_repregunta_adaptativa_sem_simular_avaliacao_acustica(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/prova-oral.md").casefold()
    assert "uma pergunta por vez" in referencia
    assert "repregunta" in referencia
    assert "ao final do ciclo" in referencia
    assert "não avalie voz" in referencia


def test_revisao_separa_assistencia_transferencia_e_retencao(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/revisao.md").casefold()
    for estado in ("com assistência", "transferência independente", "retenção posterior"):
        assert estado in referencia
