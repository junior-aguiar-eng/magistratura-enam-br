from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARQUIVOS_DISTRIBUIDOS = (
    ROOT / "AGENTS.md",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / "README.md",
    *sorted((ROOT / "skills").glob("*/SKILL.md")),
    *sorted((ROOT / "skills").glob("*/references/*.md")),
)

DEFAULTS_PESSOAIS_PROIBIDOS = (
    "50% ciclo geral",
    "25% recuperação",
    "empresarial/humanística/direitos humanos",
    "na última vez em que fizemos essa escolha",
    "seu estágio atual",
)


def test_distribuicao_nao_embute_percurso_pessoal_do_autor():
    corpus = "\n".join(path.read_text(encoding="utf-8").casefold() for path in ARQUIVOS_DISTRIBUIDOS)
    for trecho in DEFAULTS_PESSOAIS_PROIBIDOS:
        assert trecho.casefold() not in corpus


def test_plugin_continua_especializado_em_bachareis_e_magistratura():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").casefold()
    assert "bachar" in agents
    assert "magistratura" in agents
    assert "não simplifique" in agents
