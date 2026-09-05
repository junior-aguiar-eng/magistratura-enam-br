from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "acompanhar-percurso-magistratura"


def test_pedido_generico_recebe_apresentacao_breve_das_cinco_frentes():
    protocolo = (SKILL_DIR / "references" / "ambientacao-conversacional.md").read_text(encoding="utf-8")

    assert "somente quando" in protocolo
    for frente in ("estudo e questões", "curadoria de informativos", "comparação de materiais", "planejamento de jurisprudência", "acompanhamento do percurso"):
        assert frente in protocolo
    assert "no máximo uma pergunta compacta" in protocolo
    assert "menu numerado, formulário ou entrevista" in protocolo


def test_pedido_especifico_ignora_ambientacao_e_nao_escolhe_tema():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    protocolo = (SKILL_DIR / "references" / "ambientacao-conversacional.md").read_text(encoding="utf-8")
    texto = skill + protocolo

    assert "Se o pedido já for específico, ignore a ambientação" in skill
    assert "Ignore este protocolo" in protocolo
    assert "não inicie questão, aula, disciplina ou tema por conta própria" in texto
    assert "Não apresente menu" in skill


def test_ambientacao_nao_expoe_contrato_tecnico_por_padrao():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
    referencia = (SKILL_DIR / "references" / "roteamento.md").read_text(encoding="utf-8").lower()

    assert "nunca devem aparecer como yaml ou formulário por padrão" in referencia
    assert "salvo pedido técnico expresso do criador do plugin" in skill
