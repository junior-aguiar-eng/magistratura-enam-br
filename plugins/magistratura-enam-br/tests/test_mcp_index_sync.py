import json
import subprocess
import sys
from pathlib import Path

from mcp_server.config import LibraryConfig
from mcp_server.tools import StudyService


def _service(tmp_path: Path) -> tuple[StudyService, Path]:
    root = tmp_path / "biblioteca"
    root.mkdir()
    (root / ".estudo-juridico").mkdir()
    document = root / "civil.md"
    document.write_text("# Civil\n\nTexto inicial.", encoding="utf-8")
    config = LibraryConfig(
        library_root=root.resolve(),
        excluded_directories=(".git", ".estudo-juridico", "node_modules"),
        max_file_bytes=2_000_000,
        max_result_chunks=12,
    )
    return StudyService(config), document


def test_verificacao_sem_mudancas_nao_regrava_indice(tmp_path: Path) -> None:
    service, _ = _service(tmp_path)
    service.index_library(confirmed=True)
    before = service.index_path.read_bytes()
    before_mtime = service.index_path.stat().st_mtime_ns

    result = service.sync_if_changed()

    assert result == {"status": "unchanged", "document_count": 1}
    assert service.index_path.read_bytes() == before
    assert service.index_path.stat().st_mtime_ns == before_mtime


def test_verificacao_incidental_inclui_novo_md_e_remove_ausente(tmp_path: Path) -> None:
    service, old_document = _service(tmp_path)
    service.index_library(confirmed=True)
    old_document.unlink()
    new_document = old_document.with_name("penal.md")
    new_document.write_text("# Penal\n\nNovo texto.", encoding="utf-8")

    result = service.sync_if_changed()

    manifest = json.loads(service.index_path.read_text(encoding="utf-8"))
    assert result == {
        "status": "updated",
        "document_count": 1,
        "indexed_count": 1,
        "removed_count": 1,
    }
    assert [document["relative_path"] for document in manifest["documents"]] == [
        "penal.md"
    ]


def test_verificacao_atualiza_md_modificado(tmp_path: Path) -> None:
    service, document = _service(tmp_path)
    service.index_library(confirmed=True)
    document.write_text("# Civil\n\nTexto atualizado.", encoding="utf-8")

    result = service.sync_if_changed()

    manifest = json.loads(service.index_path.read_text(encoding="utf-8"))
    assert result["status"] == "updated"
    assert result["indexed_count"] == 1
    assert "Texto atualizado." in manifest["documents"][0]["chunks"][0]["text"]


def test_verificacao_nao_repara_indice_ausente_ou_invalido(tmp_path: Path) -> None:
    service, _ = _service(tmp_path)

    assert service.sync_if_changed() == {"status": "missing"}
    assert not service.index_path.exists()

    service.index_path.write_text("{invalido", encoding="utf-8")
    assert service.sync_if_changed() == {"status": "invalid"}
    assert service.index_path.read_text(encoding="utf-8") == "{invalido"


def test_comando_de_uma_execucao_sincroniza_e_encerra(tmp_path: Path) -> None:
    service, document = _service(tmp_path)
    service.index_library(confirmed=True)
    document.write_text("# Civil\n\nMudança detectada.", encoding="utf-8")
    config_path = tmp_path / "library-config.json"
    config_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "library_root": str(service.config.library_root),
                "write_consent": True,
                "excluded_directories": list(service.config.excluded_directories),
                "limits": {"max_file_bytes": 2_000_000, "max_result_chunks": 12},
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "mcp_server.index_sync", "--config", str(config_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "status": "updated",
        "document_count": 1,
        "indexed_count": 1,
        "removed_count": 0,
    }
    assert "Mudança detectada." in service.index_path.read_text(encoding="utf-8")


def test_comando_sinaliza_indice_ausente_sem_cria_lo(tmp_path: Path) -> None:
    service, _ = _service(tmp_path)
    config_path = tmp_path / "library-config.json"
    config_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "library_root": str(service.config.library_root),
                "write_consent": True,
                "excluded_directories": list(service.config.excluded_directories),
                "limits": {"max_file_bytes": 2_000_000, "max_result_chunks": 12},
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "mcp_server.index_sync", "--config", str(config_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 2
    assert json.loads(result.stdout) == {"status": "missing"}
    assert not service.index_path.exists()
