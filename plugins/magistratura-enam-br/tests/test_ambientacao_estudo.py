def test_skill_roteia_ambientacao_sem_interrogatorio(texto):
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")
    protocolo = texto("skills/estudar-direito-magistratura/references/ambientacao-e-calibracao.md")

    assert "references/ambientacao-e-calibracao.md" in skill
    assert "no máximo uma pergunta" in protocolo
    assert "pedido e o material disponíveis" in protocolo
    assert "não inferir confiança, histórico ou domínio" in protocolo


def test_protocolo_distingue_quatro_contextos_e_formatos_de_resposta(texto):
    protocolo = texto("skills/estudar-direito-magistratura/references/ambientacao-e-calibracao.md")

    for titulo in ("Tema claro sem perfil", "Perfil fornecido", "Perfil desatualizado", "Persistência recusada"):
        assert f"### {titulo}" in protocolo
    assert "letra simples" in protocolo
    assert "resposta + confiança + fundamento" in protocolo

