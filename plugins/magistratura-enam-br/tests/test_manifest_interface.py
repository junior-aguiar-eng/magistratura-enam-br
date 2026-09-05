import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTENCOES = {
    "jornada": "Apresente o ambiente e ajude-me a escolher um percurso.",
    "tema": "Quero estudar um tema jurídico em profundidade.",
    "treino": "Quero treinar com uma questão jurídica difícil.",
    "informativos": "Quero curar um informativo oficial do STF ou STJ.",
    "comparacao": "Quero comparar duas versões de material do ENAM.",
    "revisao": "Quero organizar a revisão dos julgados que já selecionei.",
}


def carregar_manifesto():
    return json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))


def valor_yaml(caminho, chave):
    prefixo = f"  {chave}:"
    linha = next(item for item in caminho.read_text(encoding="utf-8").splitlines() if item.startswith(prefixo))
    return linha.split(":", 1)[1].strip().strip('"')


def test_manifesto_expoe_tres_prompts_visiveis_validos():
    prompts = carregar_manifesto()["interface"]["defaultPrompt"]
    assert prompts == [INTENCOES["jornada"], INTENCOES["tema"], INTENCOES["treino"]]
    assert all(0 < len(item) <= 128 for item in prompts)
    assert "Apresente o ambiente" in prompts[0]
    assert all("Apresente o ambiente" not in item for item in prompts[1:])


def test_gatilhos_especializados_completam_as_seis_intencoes():
    destinos = {
        "acompanhar-percurso-magistratura": INTENCOES["jornada"],
        "curar-informativos-stf-stj": INTENCOES["informativos"],
        "comparar-materiais-enam": INTENCOES["comparacao"],
        "planejar-jurisprudencia": INTENCOES["revisao"],
    }
    for skill, esperado in destinos.items():
        arquivo = ROOT / "skills" / skill / "agents" / "openai.yaml"
        assert valor_yaml(arquivo, "default_prompt") == esperado


def test_icones_do_plugin_e_das_skills_resolvem_em_assets():
    interface = carregar_manifesto()["interface"]
    for chave in ("composerIcon", "logo", "logoDark"):
        relativo = interface[chave]
        assert relativo.startswith("./assets/")
        assert (ROOT / relativo).is_file()

    for arquivo in (ROOT / "skills").glob("*/agents/openai.yaml"):
        raiz_skill = arquivo.parents[1]
        for chave in ("icon_small", "icon_large"):
            relativo = valor_yaml(arquivo, chave)
            assert ".." not in Path(relativo).parts
            assert relativo.startswith("assets/")
            assert (raiz_skill / relativo).is_file()


def test_gatilho_de_revisao_nao_abre_formulario():
    texto = (ROOT / "skills" / "planejar-jurisprudencia" / "SKILL.md").read_text(encoding="utf-8")
    assert "solicite apenas a lista, CSV ou planilha" in texto
    assert "Não antecipe questionário" in texto
