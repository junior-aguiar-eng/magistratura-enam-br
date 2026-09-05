import os
from pathlib import Path

import pytest

from mcp_server.paths import PathSecurityError, resolve_read_path, resolve_state_path


def test_resolve_arquivo_regular_dentro_da_raiz(tmp_path):
    raiz = tmp_path / "biblioteca"
    arquivo = raiz / "civil" / "obrigacoes.md"
    arquivo.parent.mkdir(parents=True)
    arquivo.write_text("# Obrigações", encoding="utf-8")

    assert resolve_read_path(raiz, Path("civil/obrigacoes.md")) == arquivo.resolve()


@pytest.mark.parametrize(
    "candidato",
    [Path("../segredo.md"), Path("civil/../../segredo.md")],
)
def test_rejeita_travessia_lexical(tmp_path, candidato):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()

    with pytest.raises(PathSecurityError, match="travessia"):
        resolve_read_path(raiz, candidato)


def test_rejeita_caminho_absoluto_externo(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    externo = tmp_path / "externo.md"
    externo.write_text("fora", encoding="utf-8")

    with pytest.raises(PathSecurityError, match="fora da biblioteca"):
        resolve_read_path(raiz, externo)


@pytest.mark.skipif(os.name != "nt", reason="contrato específico do Windows")
def test_rejeita_unc_nao_autorizado(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()

    with pytest.raises(PathSecurityError, match="UNC"):
        resolve_read_path(raiz, Path(r"\\servidor\compartilhamento\arquivo.md"))


def test_rejeita_link_que_escapa_da_raiz(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    externo = tmp_path / "externo"
    externo.mkdir()
    (externo / "segredo.md").write_text("fora", encoding="utf-8")
    link = raiz / "atalho"
    try:
        link.symlink_to(externo, target_is_directory=True)
    except OSError as erro:
        pytest.skip(f"symlink indisponível neste Windows: {erro}")

    with pytest.raises(PathSecurityError, match="fora da biblioteca"):
        resolve_read_path(raiz, Path("atalho/segredo.md"))


def test_rejeita_diretorio_e_arquivo_nao_markdown(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    (raiz / "pasta").mkdir()
    (raiz / "texto.txt").write_text("texto", encoding="utf-8")

    with pytest.raises(PathSecurityError, match="arquivo Markdown regular"):
        resolve_read_path(raiz, Path("pasta"))
    with pytest.raises(PathSecurityError, match="arquivo Markdown regular"):
        resolve_read_path(raiz, Path("texto.txt"))


def test_escrita_so_pode_atingir_subpasta_reservada(tmp_path):
    raiz = tmp_path / "biblioteca"
    estado = raiz / ".estudo-juridico"
    estado.mkdir(parents=True)

    assert resolve_state_path(raiz, Path("index.json")) == (estado / "index.json").resolve()

    with pytest.raises(PathSecurityError, match="estado local"):
        resolve_state_path(raiz, Path("../originais.md"))


def test_resolucao_de_estado_nao_cria_subpasta(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()

    with pytest.raises(PathSecurityError, match="não existe"):
        resolve_state_path(raiz, Path("index.json"))
    assert not (raiz / ".estudo-juridico").exists()
