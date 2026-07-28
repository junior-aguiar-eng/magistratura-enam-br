from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ESTADOS = {
    "confirmado",
    "confirmado com ressalvas",
    "restringido ou distinguido",
    "superado",
    "controvertido",
    "não verificado",
}
CONFIANCAS = {"alto", "médio", "baixo"}
PADRAO_NUMERO = re.compile(r"\bn[ºo°.]*\s*", re.IGNORECASE)
MODELOS = Path(__file__).resolve().parents[1] / "modelos"


def texto(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalizar_processo(value: Any) -> str:
    value = PADRAO_NUMERO.sub("", texto(value)).upper()
    return re.sub(r"[^A-Z0-9]", "", value)


def normalizar_chave(value: Any) -> str:
    value = texto(value).upper()
    value = re.sub(r"\s+", " ", value)
    return re.sub(r"[^A-Z0-9À-Ý ]", "", value).strip()


def identificador_decisao(item: dict[str, Any]) -> str:
    explicit = texto(item.get("id_decisao"))
    if explicit:
        return normalizar_chave(explicit)
    partes = [
        normalizar_chave(item.get("tribunal")),
        normalizar_processo(item.get("processo")),
        normalizar_chave(item.get("orgao_julgador")),
        texto(item.get("data_julgamento")),
        normalizar_chave(item.get("tese_resumida")),
    ]
    return "|".join(partes)


def validar_data_iso(value: Any, campo: str, contexto: str = "") -> None:
    value = texto(value)
    if not value:
        return
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        prefixo = f"{contexto}: " if contexto else ""
        raise ValueError(f"{prefixo}'{campo}' deve usar AAAA-MM-DD.") from exc


def validar_schema(nome: str, instancia: Any) -> None:
    schema = json.loads((MODELOS / nome).read_text(encoding="utf-8"))
    erros = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instancia),
        key=lambda erro: list(erro.absolute_path),
    )
    if not erros:
        return
    erro = erros[0]
    caminho = ".".join(str(parte) for parte in erro.absolute_path) or "raiz"
    raise ValueError(f"Contrato {nome} violado em {caminho}: {erro.message}")


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
