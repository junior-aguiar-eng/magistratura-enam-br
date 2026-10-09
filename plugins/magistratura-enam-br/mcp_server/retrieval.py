import re
import unicodedata

from .config import LibraryConfig

TOKEN = re.compile(r"[^\W_]+", re.UNICODE)


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def _terms(query: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(TOKEN.findall(_normalize(query))))


def _normalized_content(value: str, cache: dict[str, str] | None) -> str:
    if cache is None:
        return _normalize(value)
    normalized = cache.get(value)
    if normalized is None:
        normalized = _normalize(value)
        cache[value] = normalized
    return normalized


def search_index(
    manifest: dict,
    query: str,
    *,
    limit: int,
    config: LibraryConfig,
    path_prefix: str | None = None,
    normalized_content: dict[str, str] | None = None,
) -> list[dict]:
    terms = _terms(query)
    if not terms or limit <= 0:
        return []

    prefix = path_prefix.replace("\\", "/").casefold() if path_prefix else None
    matches: list[dict] = []
    for document in manifest.get("documents", []):
        relative_path = document["relative_path"]
        if prefix is not None and not relative_path.casefold().startswith(prefix):
            continue
        for chunk in document.get("chunks", []):
            heading = chunk.get("heading") or ""
            normalized_heading = _normalized_content(heading, normalized_content)
            normalized_text = _normalized_content(chunk["text"], normalized_content)
            score = sum(3 * normalized_heading.count(term) + normalized_text.count(term) for term in terms)
            if score == 0:
                continue
            matches.append(
                {
                    "document_id": document["document_id"],
                    "chunk_id": chunk["chunk_id"],
                    "relative_path": relative_path,
                    "heading": chunk.get("heading"),
                    "text": chunk["text"],
                    "score": score,
                }
            )
    matches.sort(key=lambda item: (-item["score"], item["relative_path"].casefold(), item["chunk_id"]))
    return matches[: min(limit, config.max_result_chunks)]
