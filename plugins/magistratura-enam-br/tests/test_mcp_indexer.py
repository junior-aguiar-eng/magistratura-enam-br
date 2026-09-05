import hashlib
from pathlib import Path

from mcp_server.config import LibraryConfig
from mcp_server.indexer import index_library


def config(raiz: Path, max_file_bytes: int = 2_000_000) -> LibraryConfig:
    return LibraryConfig(
        library_root=raiz.resolve(),
        excluded_directories=(".git", ".estudo-juridico", "node_modules"),
        max_file_bytes=max_file_bytes,
        max_result_chunks=12,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_indexa_markdown_recursivamente_com_headings_e_unicode(tmp_path):
    raiz = tmp_path / "biblioteca"
    civil = raiz / "civil" / "obrigações.md"
    civil.parent.mkdir(parents=True)
    civil.write_text(
        "# Obrigações\n\nIntrodução geral.\n\n## Inadimplemento\n\nMora e perdas e danos.",
        encoding="utf-8",
    )

    resultado = index_library(config(raiz))

    assert resultado.indexed_count == 1
    assert resultado.reused_count == 0
    documento = resultado.manifest["documents"][0]
    assert documento["relative_path"] == "civil/obrigações.md"
    assert documento["title"] == "Obrigações"
    assert [chunk["heading"] for chunk in documento["chunks"]] == ["Obrigações", "Inadimplemento"]
    assert documento["sha256"] == sha256(civil)


def test_ignora_pastas_reservadas_ocultas_exclusoes_e_arquivo_grande(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    (raiz / "válido.md").write_text("# Válido\n\nConteúdo.", encoding="utf-8")
    for nome in (".git", ".estudo-juridico", "node_modules", ".oculta"):
        pasta = raiz / nome
        pasta.mkdir()
        (pasta / "ignorado.md").write_text("# Ignorado", encoding="utf-8")
    (raiz / "grande.md").write_text("x" * 200, encoding="utf-8")
    (raiz / "texto.txt").write_text("não indexar", encoding="utf-8")

    resultado = index_library(config(raiz, max_file_bytes=100))

    assert [item["relative_path"] for item in resultado.manifest["documents"]] == ["válido.md"]
    assert {item["relative_path"] for item in resultado.ignored_files} == {
        ".estudo-juridico/ignorado.md",
        ".git/ignorado.md",
        ".oculta/ignorado.md",
        "grande.md",
        "node_modules/ignorado.md",
    }


def test_reutiliza_documento_inalterado_e_remove_entrada_ausente(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    mantido = raiz / "mantido.md"
    removido = raiz / "removido.md"
    mantido.write_text("# Mantido\n\nTexto estável.", encoding="utf-8")
    removido.write_text("# Removido\n\nTexto.", encoding="utf-8")
    inicial = index_library(config(raiz))
    removido.unlink()

    atualizado = index_library(config(raiz), previous_manifest=inicial.manifest)

    assert atualizado.indexed_count == 0
    assert atualizado.reused_count == 1
    assert atualizado.removed_count == 1
    assert atualizado.manifest["documents"] == [
        next(item for item in inicial.manifest["documents"] if item["relative_path"] == "mantido.md")
    ]


def test_indexacao_nao_altera_os_markdown(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    arquivos = [raiz / "a.md", raiz / "b.md"]
    for indice, arquivo in enumerate(arquivos):
        arquivo.write_text(f"# Documento {indice}\n\nConteúdo {indice}.", encoding="utf-8")
    hashes_antes = {arquivo: sha256(arquivo) for arquivo in arquivos}

    index_library(config(raiz))

    assert {arquivo: sha256(arquivo) for arquivo in arquivos} == hashes_antes

