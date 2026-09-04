#!/usr/bin/env python3
"""Log local append-only de eventos pedagógicos."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).resolve().parents[1] / "modelos/pedagogia/learning-event.schema.json"


def validar_evento(evento: dict) -> list[str]:
    if not isinstance(evento, dict):
        return ["evento deve ser objeto JSON"]
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [e.message for e in sorted(validator.iter_errors(evento), key=lambda e: list(e.path))]


def ler_eventos(caminho: Path) -> list[dict]:
    resultado, ids = [], set()
    with Path(caminho).open(encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, 1):
            try:
                evento = json.loads(linha)
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON corrompido na linha {numero}: {exc.msg}") from exc
            erros = validar_evento(evento)
            if erros:
                raise ValueError(f"Evento inválido na linha {numero}: {'; '.join(erros)}")
            if evento["event_id"] in ids:
                raise ValueError(f"event_id duplicado na linha {numero}: {evento['event_id']}")
            ids.add(evento["event_id"])
            resultado.append(evento)
    return resultado


def acrescentar_evento(caminho: Path, evento: dict, *, criar_diretorio: bool = False) -> None:
    caminho = Path(caminho)
    erros = validar_evento(evento)
    if erros:
        raise ValueError(f"Evento inválido: {'; '.join(erros)}")
    if not caminho.parent.is_dir():
        if not criar_diretorio:
            raise FileNotFoundError(f"Diretório do log não existe: {caminho.parent}")
        caminho.parent.mkdir(parents=True)
    existentes = ler_eventos(caminho) if caminho.exists() else []
    if any(e["event_id"] == evento["event_id"] for e in existentes):
        raise ValueError(f"event_id duplicado: {evento['event_id']}")
    with caminho.open("a", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(json.dumps(evento, ensure_ascii=False, separators=(",", ":")) + "\n")
        arquivo.flush()
        os.fsync(arquivo.fileno())


def _objeto(caminho: Path) -> dict:
    dado = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(dado, dict):
        raise TypeError("Arquivo deve conter objeto JSON.")
    return dado


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="comando", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--evento", type=Path, required=True)
    append = sub.add_parser("append")
    append.add_argument("--log", type=Path, required=True)
    append.add_argument("--evento", type=Path, required=True)
    append.add_argument("--criar-diretorio", action="store_true")
    args = parser.parse_args(argv)
    evento = _objeto(args.evento)
    if args.comando == "validate":
        erros = validar_evento(evento)
        print(json.dumps({"status": "aprovado" if not erros else "reprovado", "erros": erros,}, ensure_ascii=False))
        return 0 if not erros else 2
    acrescentar_evento(args.log, evento, criar_diretorio=args.criar_diretorio)
    print(json.dumps({"status": "registrado", "event_id": evento["event_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
