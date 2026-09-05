from pathlib import Path

STATE_DIRECTORY = ".estudo-juridico"


class PathSecurityError(ValueError):
    """Caminho viola os limites da biblioteca autorizada."""


def _has_parent_traversal(candidate: Path) -> bool:
    return ".." in candidate.parts


def _is_unc(candidate: Path) -> bool:
    return str(candidate).startswith(("\\\\", "//"))


def _ensure_contained(path: Path, boundary: Path, message: str) -> None:
    if not path.is_relative_to(boundary):
        raise PathSecurityError(message)


def resolve_read_path(root: Path, candidate: Path) -> Path:
    library_root = Path(root).resolve(strict=True)
    requested = Path(candidate)
    if _is_unc(requested) and not _is_unc(library_root):
        raise PathSecurityError("Caminho UNC não autorizado")
    if _has_parent_traversal(requested):
        raise PathSecurityError("travessia de diretório não permitida")

    resolved = requested.resolve(strict=True) if requested.is_absolute() else (library_root / requested).resolve(strict=True)
    _ensure_contained(resolved, library_root, "Caminho fora da biblioteca autorizada")
    if not resolved.is_file() or resolved.suffix.casefold() != ".md":
        raise PathSecurityError("O alvo deve ser um arquivo Markdown regular")
    return resolved


def resolve_state_path(root: Path, candidate: Path) -> Path:
    library_root = Path(root).resolve(strict=True)
    state_root = library_root / STATE_DIRECTORY
    if not state_root.is_dir():
        raise PathSecurityError("A subpasta de estado local não existe")

    requested = Path(candidate)
    if requested.is_absolute() or _has_parent_traversal(requested):
        raise PathSecurityError("Caminho fora da subpasta de estado local")
    resolved = (state_root / requested).resolve(strict=False)
    _ensure_contained(resolved, state_root.resolve(strict=True), "Caminho fora da subpasta de estado local")
    return resolved
