"""Executa uma verificação pontual do índice local."""

import argparse
import json
from pathlib import Path

from .config import LibraryConfig
from .tools import StudyService


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verificar e sincronizar índice Markdown uma vez"
    )
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)

    result = StudyService(LibraryConfig.load(args.config)).sync_if_changed()
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"unchanged", "updated"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
