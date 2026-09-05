from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    nome: (ROOT / "skills" / nome / "SKILL.md").read_text(encoding="utf-8")
    for nome in (
        "estudar-direito-magistratura",
        "curar-informativos-stf-stj",
        "comparar-materiais-enam",
        "planejar-jurisprudencia",
    )
}


def test_skills_juridicas_adotam_contrato_e_apresentacao_comuns():
    for texto in SKILLS.values():
        assert "politica-fontes-juridicas.md" in texto
        assert "protocolo-uso-do-acervo.md" in texto
        assert "Base consultada" in texto
        assert "editorial" in texto.lower()


def test_estudo_separa_acervo_complemento_e_atualizacao():
    texto = SKILLS["estudar-direito-magistratura"]
    assert "acervo como base pedagógica" in texto
    assert "separação entre conteúdo do candidato, complemento e atualização oficial" in texto
    assert "não faça busca nem complemento externo" in texto


def test_curadoria_exige_informativo_oficial():
    texto = SKILLS["curar-informativos-stf-stj"]
    assert "exige o informativo oficial do STF ou STJ como fonte determinante" in texto
    assert "julgamento noticiado, não como tese confirmada" in texto


def test_comparacao_exclusiva_nao_introduz_pesquisa():
    texto = SKILLS["comparar-materiais-enam"]
    assert "não introduza pesquisa externa" in texto
    assert "não use conhecimento externo para classificar delta" in texto


def test_planejamento_nao_pesquisa_novos_julgados():
    texto = SKILLS["planejar-jurisprudencia"]
    assert "não pesquise novo julgado, mérito, atualização ou substituto" in texto
    assert "devolva a autoridade ao orquestrador" in texto


def test_transicao_de_politica_depende_de_mudanca_real_de_escopo():
    for nome in (
        "estudar-direito-magistratura",
        "curar-informativos-stf-stj",
        "comparar-materiais-enam",
    ):
        texto = SKILLS[nome].lower()
        assert "efetivamente" in texto
        assert "fontes" in texto
