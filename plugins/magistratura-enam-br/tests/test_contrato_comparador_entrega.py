from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def texto(relativo: str) -> str:
    return (RAIZ / relativo).read_text(encoding="utf-8")


def test_comparador_entrega_tabela_no_chat_sem_artefato_padrao():
    skill = texto("skills/comparar-materiais-enam/SKILL.md")
    formato = texto("skills/comparar-materiais-enam/references/formato-entrega-comparativo.md")

    assert "tabela didática no chat" in skill
    assert "não crie nem cite arquivos de saída por padrão" in skill
    assert "| Capítulo / tema | Material anterior | Material novo |" in formato
    assert "Não repita a tabela em prosa" in formato
