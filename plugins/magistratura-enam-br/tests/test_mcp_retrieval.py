from pathlib import Path

from mcp_server.config import LibraryConfig
from mcp_server.indexer import index_library
from mcp_server.retrieval import search_index


def criar_indice(tmp_path: Path) -> tuple[dict, LibraryConfig]:
    raiz = tmp_path / "biblioteca"
    civil = raiz / "civil"
    penal = raiz / "penal"
    civil.mkdir(parents=True)
    penal.mkdir()
    (civil / "prescricao.md").write_text(
        "# Prescrição\n\nA pretensão nasce com a violação do direito.\n\n## Termo inicial\n\nActio nata.",
        encoding="utf-8",
    )
    (penal / "prescricao.md").write_text(
        "# Prescrição penal\n\nA prescrição penal extingue a punibilidade.",
        encoding="utf-8",
    )
    cfg = LibraryConfig(
        library_root=raiz.resolve(),
        excluded_directories=(".git", ".estudo-juridico", "node_modules"),
        max_file_bytes=2_000_000,
        max_result_chunks=2,
    )
    return index_library(cfg).manifest, cfg


def test_busca_lexical_ordena_resultados_e_preserva_rastreabilidade(tmp_path):
    manifesto, cfg = criar_indice(tmp_path)

    resultados = search_index(manifesto, "violação direito", limit=10, config=cfg)

    assert resultados[0]["relative_path"] == "civil/prescricao.md"
    assert resultados[0]["heading"] == "Prescrição"
    assert resultados[0]["score"] > 0
    assert {"document_id", "chunk_id", "text"} <= resultados[0].keys()


def test_busca_respeita_limite_da_configuracao_e_filtro_de_pasta(tmp_path):
    manifesto, cfg = criar_indice(tmp_path)

    resultados = search_index(
        manifesto,
        "prescrição",
        limit=20,
        config=cfg,
        path_prefix="penal/",
    )

    assert len(resultados) == 1
    assert resultados[0]["relative_path"] == "penal/prescricao.md"


def test_busca_vazia_nao_devolve_todo_o_acervo(tmp_path):
    manifesto, cfg = criar_indice(tmp_path)

    assert search_index(manifesto, "   ", limit=10, config=cfg) == []
