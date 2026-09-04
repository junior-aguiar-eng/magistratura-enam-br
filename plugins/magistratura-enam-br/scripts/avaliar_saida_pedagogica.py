#!/usr/bin/env python3
"""Executa somente verificações estruturais das avaliações pedagógicas."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

PADRAO_ALTERNATIVA = re.compile(r"(?im)^\s*([A-E])[.)]\s+\S")


def normalizar(texto: str) -> str:
    decomposicao = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(caractere for caractere in decomposicao if not unicodedata.combining(caractere))


def verificar(assertion: dict, texto: str) -> tuple[bool, str]:
    check = assertion.get("check")
    values = assertion.get("values", [])
    texto_normalizado = normalizar(texto)

    if check == "contains_all":
        ausentes = [valor for valor in values if normalizar(valor) not in texto_normalizado]
        return not ausentes, "ausentes: " + ", ".join(ausentes) if ausentes else "todos os marcadores presentes"

    if check == "forbidden_terms":
        encontrados = [valor for valor in values if normalizar(valor) in texto_normalizado]
        return not encontrados, "encontrados: " + ", ".join(encontrados) if encontrados else "nenhum termo proibido"

    if check == "option_count":
        letras = PADRAO_ALTERNATIVA.findall(texto)
        esperado = int(assertion.get("expected", 5))
        return len(letras) == esperado, f"alternativas encontradas: {len(letras)}; esperado: {esperado}"

    if check == "ends_after_option_e":
        linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        passou = bool(linhas and re.match(r"(?i)^E[.)]\s+\S", linhas[-1]))
        return passou, "última linha é a alternativa E" if passou else "há conteúdo após a alternativa E ou ela está ausente"

    if check == "ordered_markers":
        posicoes = [texto_normalizado.find(normalizar(valor)) for valor in values]
        passou = all(posicao >= 0 for posicao in posicoes) and posicoes == sorted(posicoes)
        return passou, f"posições: {posicoes}"

    return False, f"verificação automática desconhecida: {check}"


def avaliar_saida(caso: dict, texto: str) -> dict:
    resultados = []
    revisao_humana = []
    for assertion in caso.get("assertions", []):
        if assertion.get("kind") == "human":
            revisao_humana.append(assertion["id"])
            continue
        passou, evidencia = verificar(assertion, texto)
        resultados.append({
            "id": assertion["id"],
            "description": assertion["description"],
            "passed": passou,
            "evidence": evidencia,
        })

    if any(not item["passed"] for item in resultados):
        status = "reprovado"
    elif revisao_humana:
        status = "revisao_humana_pendente"
    else:
        status = "aprovado_estruturalmente"
    return {
        "case_id": caso.get("id"),
        "status": status,
        "assertions": resultados,
        "human_review_required": revisao_humana,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Avalia a estrutura de uma saída pedagógica.")
    parser.add_argument("--catalogo", type=Path, required=True)
    parser.add_argument("--caso", required=True)
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()

    catalogo = json.loads(args.catalogo.read_text(encoding="utf-8"))
    caso = next((item for item in catalogo["evals"] if item["id"] == args.caso), None)
    if caso is None:
        raise SystemExit(f"Caso não encontrado: {args.caso}")
    texto = args.saida.read_text(encoding="utf-8")
    print(json.dumps(avaliar_saida(caso, texto), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
