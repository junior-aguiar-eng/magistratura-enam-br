def test_markdown_e_a_fonte_pedagogica_preferencial(texto):
    assert "Markdown é a fonte pedagógica preferencial" in texto("AGENTS.md")
    assert "leia e use primeiro o Markdown" in texto(
        "references/protocolo-uso-do-acervo.md"
    )
    assert "comece pelo Markdown" in texto(
        "skills/estudar-direito-magistratura/SKILL.md"
    )


def test_pdf_permanece_plano_b_sem_deslocar_fontes_oficiais(texto):
    protocolo = texto("references/protocolo-uso-do-acervo.md")
    assert "Consulte o PDF apenas como plano B" in protocolo
    assert "use a fonte oficial original adequada, ainda que em PDF" in protocolo
