from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_comparador_exporta_evento_so_sob_pedido_e_sem_calendarizacao():
    skill = (ROOT / "skills/comparar-materiais-enam/SKILL.md").read_text(encoding="utf-8")
    formato = (
        ROOT / "skills/comparar-materiais-enam/references/formato-entrega-comparativo.md"
    ).read_text(encoding="utf-8")
    texto = (skill + formato).lower()

    assert "material_atualizado" in texto
    assert "somente mediante pedido expresso" in texto
    assert "não atribua data, intervalo ou prioridade" in texto
    assert "julgado já presente na esteira" in texto
