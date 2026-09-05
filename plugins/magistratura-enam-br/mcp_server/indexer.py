import hashlib
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .config import LibraryConfig
from .paths import PathSecurityError, resolve_read_path

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class IndexingResult:
    manifest: dict
    indexed_count: int
    reused_count: int
    removed_count: int
    ignored_files: tuple[dict, ...]


def _identifier(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_excluded(relative: Path, exclusions: set[str]) -> bool:
    return any(part in exclusions or part.startswith(".") for part in relative.parts[:-1])


def _discover_markdown(config: LibraryConfig) -> tuple[list[Path], list[dict]]:
    root = config.library_root
    exclusions = set(config.excluded_directories)
    discovered: list[Path] = []
    ignored: list[dict] = []
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        relative_directory = current_path.relative_to(root)
        pruned: list[str] = []
        for directory in directories:
            relative = relative_directory / directory
            if directory in exclusions or directory.startswith("."):
                pruned.append(directory)
                for item in sorted((current_path / directory).rglob("*.md")):
                    if item.is_file():
                        ignored.append({"relative_path": _relative(item, root), "reason": "excluded_directory"})
        directories[:] = [item for item in directories if item not in pruned]

        for filename in files:
            path = current_path / filename
            if path.suffix.casefold() != ".md":
                continue
            relative = path.relative_to(root)
            if _is_excluded(relative, exclusions):
                ignored.append({"relative_path": relative.as_posix(), "reason": "excluded_directory"})
                continue
            try:
                safe_path = resolve_read_path(root, relative)
            except (OSError, PathSecurityError):
                ignored.append({"relative_path": relative.as_posix(), "reason": "unsafe_path"})
                continue
            if safe_path.stat().st_size > config.max_file_bytes:
                ignored.append({"relative_path": relative.as_posix(), "reason": "file_too_large"})
                continue
            discovered.append(safe_path)
    return sorted(discovered, key=lambda item: _relative(item, root).casefold()), sorted(
        ignored, key=lambda item: item["relative_path"].casefold()
    )


def _chunks(relative_path: str, text: str) -> tuple[str, list[dict]]:
    title = Path(relative_path).stem
    current_heading: str | None = None
    body: list[str] = []
    sections: list[tuple[str | None, str]] = []

    def flush() -> None:
        content = "\n".join(body).strip()
        if content:
            sections.append((current_heading, content))
        body.clear()

    for line in text.splitlines():
        match = HEADING.match(line)
        if match:
            flush()
            current_heading = match.group(2).strip()
            if match.group(1) == "#" and title == Path(relative_path).stem:
                title = current_heading
        else:
            body.append(line)
    flush()

    chunks = [
        {
            "chunk_id": _identifier("chk", f"{relative_path}\0{ordinal}\0{heading}\0{content}"),
            "heading": heading,
            "ordinal": ordinal,
            "text": content,
        }
        for ordinal, (heading, content) in enumerate(sections)
    ]
    return title, chunks


def _document(path: Path, root: Path, digest: str) -> dict:
    relative_path = _relative(path, root)
    stat = path.stat()
    title, chunks = _chunks(relative_path, path.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0.0",
        "document_id": _identifier("doc", relative_path),
        "relative_path": relative_path,
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat().replace("+00:00", "Z"),
        "sha256": digest,
        "title": title,
        "chunks": chunks,
    }


def index_library(config: LibraryConfig, previous_manifest: dict | None = None) -> IndexingResult:
    previous_documents = {
        item["relative_path"]: item for item in (previous_manifest or {}).get("documents", [])
    }
    paths, ignored = _discover_markdown(config)
    documents: list[dict] = []
    indexed_count = 0
    reused_count = 0
    for path in paths:
        relative_path = _relative(path, config.library_root)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        previous = previous_documents.get(relative_path)
        if previous is not None and previous.get("sha256") == digest:
            documents.append(previous)
            reused_count += 1
        else:
            documents.append(_document(path, config.library_root, digest))
            indexed_count += 1

    current_paths = {item["relative_path"] for item in documents}
    removed_count = len(set(previous_documents) - current_paths)
    manifest = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "documents": documents,
    }
    return IndexingResult(
        manifest=manifest,
        indexed_count=indexed_count,
        reused_count=reused_count,
        removed_count=removed_count,
        ignored_files=tuple(ignored),
    )
