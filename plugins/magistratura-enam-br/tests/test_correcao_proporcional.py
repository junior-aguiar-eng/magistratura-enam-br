from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_correcao_nao_reconstroi_enunciado_ausente_e_controla_extensao():
    skill = (
        ROOT / "skills" / "estudar-direito-magistratura" / "SKILL.md"
    ).read_text(encoding="utf-8")
    texto = skill.lower()

    assert "não atribua ao enunciado expressão que não foi fornecida" in texto
    assert "correção completa não significa reconstrução especulativa" in texto

