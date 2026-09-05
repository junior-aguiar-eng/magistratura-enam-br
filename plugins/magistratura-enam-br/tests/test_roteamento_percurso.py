from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "acompanhar-percurso-magistratura"


def test_skill_mantem_contrato_interno_e_responde_em_linguagem_natural():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    texto = skill.lower()

    assert "raciocínio interno" in texto
    assert "não os exponha como formulário, json ou yaml" in texto
    assert "linguagem natural" in texto
    assert "no máximo uma pergunta compacta" in texto
    assert "não escreva" in texto
    assert "não produza conteúdo jurídico substantivo" in texto
    assert "não alegue histórico" in texto


def test_roteamento_cobre_acionamento_positivo_e_near_miss_das_cinco_skills():
    referencia = (SKILL_DIR / "references" / "roteamento.md").read_text(
        encoding="utf-8"
    )
    positivo, near_miss = referencia.split("## Near-miss", maxsplit=1)
    skills = {
        "acompanhar-percurso-magistratura",
        "comparar-materiais-enam",
        "curar-informativos-stf-stj",
        "estudar-direito-magistratura",
        "planejar-jurisprudencia",
    }

    for skill in skills:
        assert skill in positivo
        assert skill in near_miss

    assert "agenda" in positivo and "planejar-jurisprudencia" in positivo
    assert "atualização documental" in positivo
    assert "comparar-materiais-enam" in positivo
    assert "mérito de um julgado" in near_miss
    assert "selecionar julgados" in near_miss
    assert "distribuir revisões" in near_miss


def test_metadados_sao_discriminantes_e_permitem_invocacao_implicita():
    metadata = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )

    assert metadata["interface"]["display_name"] == "Acompanhar percurso da Magistratura"
    assert "roteia" in metadata["interface"]["short_description"].lower()
    assert metadata["policy"]["allow_implicit_invocation"] is True


def test_recomendacao_restringe_destino_as_cinco_skills_existentes():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    referencia = (SKILL_DIR / "references" / "roteamento.md").read_text(
        encoding="utf-8"
    )
    texto = skill + referencia

    assert "nunca invente nome de skill" in texto.lower()
    assert "questões objetivas" in texto
    assert "`estudar-direito-magistratura`" in texto
    assert "elaborar-questoes-objetivas" not in texto


def test_precedencia_preserva_rota_e_reserva_pergunta_para_ambiguidade():
    referencia = (SKILL_DIR / "references" / "roteamento.md").read_text(encoding="utf-8")
    marcadores = [
        "Invocação explícita",
        "Objetivo e insumo inequívocos",
        "Continuidade da rota ativa",
        "Inferência conservadora",
        "Uma pergunta discriminante",
    ]
    posicoes = [referencia.index(item) for item in marcadores]

    assert posicoes == sorted(posicoes)
    assert "Citação incidental" in referencia
    assert "não muda a rota" in referencia
