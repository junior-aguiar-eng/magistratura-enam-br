import json
import os
from pathlib import Path

import pytest

from mcp_server.config import LibraryConfig
from mcp_server.tools import StudyService


@pytest.fixture
def service(tmp_path):
    root = tmp_path / "biblioteca"
    root.mkdir()
    (root / ".estudo-juridico").mkdir()
    (root / "civil.md").write_text(
        "# Prescrição\n\nA prescrição civil limita a pretensão.\n", encoding="utf-8"
    )
    (root / "penal.md").write_text(
        "# Prescrição\n\nA prescrição penal extingue a punibilidade.\n", encoding="utf-8"
    )
    instance = StudyService(LibraryConfig(root, (), 2_000_000, 12))
    instance.index_library(confirmed=True)
    return instance


def test_busca_aquecida_usa_indice_em_memoria_sem_reler_arquivo(service, monkeypatch):
    first = service.search("PRESCRICAO", limit=2, path_prefix=None)
    original_read = Path.read_text

    def forbid_index_read(path, *args, **kwargs):
        if path == service.index_path:
            raise AssertionError("A busca repetiu a leitura integral do índice inalterado")
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", forbid_index_read)
    second = service.search("civil", limit=1, path_prefix=None)
    assert [item["relative_path"] for item in first["results"]] == ["civil.md", "penal.md"]
    assert [item["score"] for item in first["results"]] == [4, 4]
    assert second["results"][0]["text"] == "A prescrição civil limita a pretensão."


def test_busca_aquecida_nao_renormaliza_conteudo(service, monkeypatch):
    service.search("prescrição", limit=2, path_prefix=None)
    from mcp_server import retrieval

    original_normalize = retrieval._normalize

    def normalize_query_only(value):
        if value.startswith("A prescrição") or value == "Prescrição":
            raise AssertionError("Conteúdo inalterado foi normalizado novamente")
        return original_normalize(value)

    monkeypatch.setattr(retrieval, "_normalize", normalize_query_only)
    result = service.search("punibilidade", limit=1, path_prefix="PENAL")
    assert result["results"][0]["relative_path"] == "penal.md"
    assert result["results"][0]["score"] == 1


def test_substituicao_atomica_com_mesmo_tamanho_e_mtime_invalida_cache(service):
    service.search("civil", limit=2, path_prefix=None)
    before = service.index_path.stat()
    payload = service.index_path.read_bytes().replace(b"civil", b"civel")
    replacement = service.index_path.with_suffix(".replacement")
    replacement.write_bytes(payload)
    os.utime(replacement, ns=(before.st_atime_ns, before.st_mtime_ns))
    os.replace(replacement, service.index_path)
    assert service.index_path.stat().st_size == before.st_size
    assert service.index_path.stat().st_mtime_ns == before.st_mtime_ns
    assert service.search("civil", limit=2, path_prefix=None)["results"] == []
    assert service.search("civel", limit=2, path_prefix=None)["results"][0]["relative_path"] == "civel.md"


def test_reindexacao_explicitamente_autorizada_substitui_cache(service):
    service.search("civil", limit=2, path_prefix=None)
    (service.config.library_root / "civil.md").write_text("# Civil\n\nResponsabilidade objetiva.", encoding="utf-8")
    service.index_library(confirmed=True)
    result = service.search("objetiva", limit=2, path_prefix=None)
    assert result["results"][0]["text"] == "Responsabilidade objetiva."


@pytest.mark.parametrize("mutation", ["delete", "corrupt"])
def test_indice_ausente_ou_corrompido_nao_reutiliza_conteudo_anterior(service, mutation):
    service.search("civil", limit=2, path_prefix=None)
    if mutation == "delete":
        service.index_path.unlink()
        error = FileNotFoundError
    else:
        service.index_path.write_text("{invalido", encoding="utf-8")
        error = json.JSONDecodeError
    with pytest.raises(error):
        service.search("civil", limit=2, path_prefix=None)


def test_cache_preserva_limite_prefixo_texto_e_indice_sem_gravacao(service):
    original_bytes = service.index_path.read_bytes()
    original_stat = service.index_path.stat()
    for _ in range(2):
        result = service.search("PRESCRIÇÃO prescrição", limit=20, path_prefix="PENAL")
        assert len(result["results"]) == 1
        assert result["results"][0]["heading"] == "Prescrição"
        assert result["results"][0]["text"] == "A prescrição penal extingue a punibilidade."
        assert result["results"][0]["score"] == 4
        assert service.search("   ", limit=2, path_prefix=None)["results"] == []
        assert service.search("civil", limit=0, path_prefix=None)["results"] == []
    assert service.index_path.read_bytes() == original_bytes
    assert service.index_path.stat().st_mtime_ns == original_stat.st_mtime_ns
