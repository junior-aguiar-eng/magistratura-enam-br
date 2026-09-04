from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_comentario_preserva_marcadores_editoriais_canônicos():
    skill = (
        ROOT / "skills" / "curar-informativos-stf-stj" / "SKILL.md"
    ).read_text(encoding="utf-8")

    for marcador in (
        "Situação precedental",
        "Tese:",
        "Controvérsia e contexto",
        "Base normativa",
        "Aplicação e limites",
        "Relevância para a Magistratura",
    ):
        assert marcador in skill

    assert "não dissolva esses marcadores" in skill.lower()

