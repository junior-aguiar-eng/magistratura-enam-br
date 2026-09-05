from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recusa_de_persistencia_expoe_opt_in_sem_diagnostico_lateral():
    skill = (
        ROOT / "skills" / "estudar-direito-magistratura" / "SKILL.md"
    ).read_text(encoding="utf-8")
    texto = skill.lower()

    assert "confirmação explícita e caminho local" in texto
    assert "não acrescente diagnóstico de desempenho" in texto


def test_contrato_separa_leitura_uso_gravacao_e_exclusao():
    contrato = (ROOT / "references" / "persistencia-pedagogica-local.md").read_text(encoding="utf-8").casefold()
    for operacao in ("leitura", "uso na sessão", "gravação", "exclusão"):
        assert operacao in contrato
    assert "carregar um perfil não autoriza" in contrato
