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


def test_skill_nao_inventa_recorte_ou_retomada(texto):
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")

    assert "não autoriza escolher unilateralmente subtema, modalidade, caso" in skill
    assert "não inicie aula, questão ou flashcards" in skill
    assert "não fornecer o último ponto ou checkpoint" in skill
    assert "mudança apenas de tema, preserve a modalidade" in skill
    assert "não volte a perguntar modalidade" in skill
    assert "possibilidade futura de outra atividade não cria rota" in skill
