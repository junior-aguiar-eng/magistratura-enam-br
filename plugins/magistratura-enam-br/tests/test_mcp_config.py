import json
from pathlib import Path

import pytest

from mcp_server.config import ConfigError, LibraryConfig


def escrever_config(path: Path, raiz: Path, **alteracoes) -> Path:
    dados = {
        "schema_version": "1.0.0",
        "library_root": str(raiz.resolve()),
        "write_consent": True,
        "excluded_directories": [".git", ".estudo-juridico", "node_modules"],
        "limits": {"max_file_bytes": 2_000_000, "max_result_chunks": 12},
    }
    dados.update(alteracoes)
    path.write_text(json.dumps(dados), encoding="utf-8")
    return path


def test_carrega_configuracao_versionada_sem_criar_diretorios(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    config_path = escrever_config(tmp_path / "config.json", raiz)

    config = LibraryConfig.load(config_path)

    assert config.library_root == raiz.resolve()
    assert config.max_file_bytes == 2_000_000
    assert config.max_result_chunks == 12
    assert not (raiz / ".estudo-juridico").exists()


def test_configuracao_ausente_e_rejeitada(tmp_path):
    with pytest.raises(ConfigError, match="não encontrada"):
        LibraryConfig.load(tmp_path / "ausente.json")


@pytest.mark.parametrize("raiz_invalida", ["relativa", "arquivo"])
def test_rejeita_raiz_relativa_ou_arquivo(tmp_path, raiz_invalida):
    if raiz_invalida == "arquivo":
        raiz = tmp_path / "arquivo"
        raiz.write_text("conteúdo", encoding="utf-8")
    else:
        raiz = Path("biblioteca-relativa")
    config_path = escrever_config(tmp_path / "config.json", raiz)
    if raiz_invalida == "relativa":
        dados = json.loads(config_path.read_text(encoding="utf-8"))
        dados["library_root"] = str(raiz)
        config_path.write_text(json.dumps(dados), encoding="utf-8")

    with pytest.raises(ConfigError, match="diretório absoluto existente"):
        LibraryConfig.load(config_path)


def test_rejeita_raiz_inexistente(tmp_path):
    config_path = escrever_config(tmp_path / "config.json", tmp_path / "inexistente")

    with pytest.raises(ConfigError, match="diretório absoluto existente"):
        LibraryConfig.load(config_path)


def test_rejeita_consentimento_de_escrita_nao_confirmado(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    config_path = escrever_config(tmp_path / "config.json", raiz, write_consent=False)

    with pytest.raises(ConfigError, match="consentimento"):
        LibraryConfig.load(config_path)

