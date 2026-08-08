from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def texto(relativo: str) -> str:
    return (RAIZ / relativo).read_text(encoding="utf-8")


def test_trava_fgv_e_obrigatoria_na_diretriz_e_na_skill():
    diretrizes = texto("AGENTS.md")
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")

    assert "padrão FGV/ENAM para questões objetivas é canônico e obrigatório" in diretrizes
    assert "trava canônica de emissão nela prevista como condição obrigatória" in skill
    assert "## Trava canônica FGV/ENAM" in skill
    assert "Rejeite o rascunho se a correta for a única alternativa ponderada" in skill
    assert "### Trava canônica de emissão" in referencia
    assert "### Densidade e inteligência do enunciado" in referencia
    assert "Se houver disciplina específica aplicável" in referencia
    assert "descarte o rascunho e reconstrua-o" in referencia


def test_trava_rejeita_gabarito_generico_e_racionalizacao_posterior():
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")

    assert "não use princípio, ponderação ou constitucionalização genérica" in referencia
    assert "regra específica ignorada" in referencia
    assert "não racionalize uma alternativa como correta" in referencia
    assert "tensão entre pelo menos dois planos decisivos" in referencia
    assert "dado ornamental" in referencia
    assert "### Matriz obrigatória de construção" in referencia
    assert "Não use como distrator a simples negativa" in referencia
    assert "cada distrator deve conter âncora normativa" in referencia


def test_correcao_completa_e_obrigatoria_mesmo_apos_acerto():
    diretrizes = texto("AGENTS.md")
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")
    cenarios = texto("skills/estudar-direito-magistratura/references/cenarios-avaliacao.md")

    assert "aplique uma sequência canônica, ainda que o candidato tenha acertado" in diretrizes
    assert "## Trava canônica de correção objetiva" in skill
    assert "O acerto do candidato não autoriza omitir a análise das alternativas" in skill
    assert "a correção completa é obrigatória tanto no acerto quanto no erro" in referencia
    assert "## Q6 — Correção completa após acerto" in cenarios


def test_correcao_usa_modelo_como_calibracao_sem_reproduzir_imprecisao():
    diretrizes = texto("AGENTS.md")
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")

    assert "referência de calibração do modo de perguntar e corrigir" in diretrizes
    assert "não o trate como mera preferência efêmera de estilo" in diretrizes
    assert "use-os como corpus de calibração" in referencia
    assert "Não invente “pegadinha da banca”" in referencia
