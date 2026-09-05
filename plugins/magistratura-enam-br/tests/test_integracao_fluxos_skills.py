from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "acompanhar-percurso-magistratura",
    "comparar-materiais-enam",
    "curar-informativos-stf-stj",
    "estudar-direito-magistratura",
    "planejar-jurisprudencia",
)


def texto_skill(nome):
    return (ROOT / "skills" / nome / "SKILL.md").read_text(encoding="utf-8")


def test_cinco_skills_reconhecem_protocolo_de_transicao():
    for nome in SKILLS:
        texto = texto_skill(nome)
        assert "transicoes-inteligentes.md" in texto


def test_skills_especializadas_preservam_continuidade_e_devolvem_autoridade():
    for nome in SKILLS[1:]:
        texto = texto_skill(nome)
        assert "continuidade" in texto.lower()
        assert "devolva a autoridade" in texto
        assert "não execute silenciosamente a outra skill" in texto
        assert "repetir ambientação" in texto or "repita ambientação" in texto
        assert "Entre sessões, só retome com estado ou checkpoint fornecido" in texto


def test_mudanca_de_assunto_nao_cria_evento_ou_descarta_pendencia():
    estudo = texto_skill("estudar-direito-magistratura")
    curadoria = texto_skill("curar-informativos-stf-stj")
    comparacao = texto_skill("comparar-materiais-enam")
    planejamento = texto_skill("planejar-jurisprudencia")

    assert "não registra tentativa, erro ou abandono" in estudo
    assert "não conclui boletim nem cria avaliação" in curadoria
    assert "não confirma delta, exclusão, tentativa, erro ou abandono" in comparacao
    assert "não fecha remediação, não registra tentativa e não altera a planilha" in planejamento
