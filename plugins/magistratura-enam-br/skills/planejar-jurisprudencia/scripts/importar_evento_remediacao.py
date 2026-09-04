#!/usr/bin/env python3
"""Importa um evento confirmado para fechar remediação na esteira."""

import argparse
import json
import sys
from pathlib import Path

from atualizar_esteira import importar_evento_remediacao


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Importa evento válido e confirmado na aba Remediacao."
    )
    parser.add_argument("--arquivo", type=Path, required=True)
    parser.add_argument("--evento", type=Path, required=True)
    parser.add_argument(
        "--confirmar",
        action="store_true",
        help="confirma explicitamente o fechamento persistente",
    )
    args = parser.parse_args()

    if not args.confirmar:
        parser.error("--confirmar é obrigatório para alterar a planilha")

    try:
        evento = json.loads(args.evento.read_text(encoding="utf-8"))
        concluida = importar_evento_remediacao(
            args.arquivo, evento, confirmado=True
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        sys.stderr.write(f"erro: {exc}\n")
        return 2

    if not concluida:
        sys.stderr.write(
            "evento recusado: inválido, divergente, parcial ou já processado\n"
        )
        return 1

    print("remediação concluída e persistida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
