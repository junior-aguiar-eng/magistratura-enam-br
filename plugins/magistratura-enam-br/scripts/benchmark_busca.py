"""Mede buscas locais sem escrever no acervo ou revelar o conteúdo dos resultados.

Execute na raiz do plugin: uv run python -m scripts.benchmark_busca --library CAMINHO
"""

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from time import perf_counter

from mcp_server.config import LibraryConfig
from mcp_server.tools import StudyService

QUERIES = (
    "prescricao responsabilidade civil",
    "contraditorio prova processo",
    "competencia constitucional controle",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if not 2 <= args.repeats <= 100:
        parser.error("--repeats deve ficar entre 2 e 100")
    service = StudyService(LibraryConfig(args.library.resolve(strict=True), (), 2_000_000, 12))
    before = service.index_path.stat()
    runs = []
    for iteration in range(args.repeats):
        for query in QUERIES:
            start = perf_counter()
            result = service.search(query, limit=4, path_prefix=None)
            elapsed = (perf_counter() - start) * 1000
            digest = hashlib.sha256(
                json.dumps(result, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ).hexdigest()
            runs.append({"iteration": iteration, "query": query, "ms": round(elapsed, 3), "sha256": digest})
    after = service.index_path.stat()
    print(json.dumps({
        "index_bytes": before.st_size,
        "index_unchanged": (before.st_size, before.st_mtime_ns, before.st_ino)
        == (after.st_size, after.st_mtime_ns, after.st_ino),
        "first_search_ms": runs[0]["ms"],
        "subsequent_median_ms": round(statistics.median(run["ms"] for run in runs[1:]), 3),
        "runs": runs,
        "scope": "Busca local; não mede geração do modelo, internet, túnel ou UI do ChatGPT.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
