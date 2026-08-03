"""Utilidades compartilhadas entre os scripts da esteira de jurisprudência."""

from __future__ import annotations

from typing import Any


def sanitizar_excel(value: Any) -> Any:
    if value is None:
        return ""
    if not isinstance(value, str):
        return value
    # Não remover espaços antes da inspeção: fórmulas podem ser ocultadas por whitespace.
    stripped = value.lstrip()
    if stripped.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value.strip()
