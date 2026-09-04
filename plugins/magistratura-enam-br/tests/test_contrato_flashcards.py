def test_flashcard_e_atomico_avaliavel_e_rastreavel(texto):
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")
    contrato = texto("skills/estudar-direito-magistratura/references/flashcards-de-alto-rendimento.md")

    assert "references/flashcards-de-alto-rendimento.md" in skill
    assert "uma decisão recuperável" in contrato
    assert "Pergunta discriminativa" in contrato
    assert "Resposta independente" in contrato
    assert "Fonte identificável" in contrato
    assert "cartão meramente opinativo" in contrato


def test_flashcards_nao_sao_rituais_nem_eventos_antecipados(texto):
    contrato = texto("skills/estudar-direito-magistratura/references/flashcards-de-alto-rendimento.md")

    assert "no máximo três" in contrato
    assert "omita os cartões" in contrato
    assert "tentativa posterior" in contrato

