from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recusa_de_persistencia_expoe_opt_in_sem_diagnostico_lateral():
    skill = (
        ROOT / "skills" / "estudar-direito-magistratura" / "SKILL.md"
    ).read_text(encoding="utf-8")
    texto = skill.lower()

    assert "confirmação explícita e caminho local" in texto
    assert "não acrescente diagnóstico de desempenho" in texto

