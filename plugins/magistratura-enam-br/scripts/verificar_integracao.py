#!/usr/bin/env python3
"""Verifica a integridade operacional da versão consolidada do plugin."""

from __future__ import annotations

import argparse
import json
import py_compile
from pathlib import Path


ARQUIVOS_ESSENCIAIS = (
    ".codex-plugin/plugin.json",
    "requirements.txt",
    "skills/curar-informativos-stf-stj/SKILL.md",
    "skills/curar-informativos-stf-stj/modelos/precedentes.schema.json",
    "skills/curar-informativos-stf-stj/scripts/atualizar_planilha_precedentes.py",
    "skills/estudar-direito-magistratura/SKILL.md",
    "skills/planejar-jurisprudencia/SKILL.md",
    "skills/planejar-jurisprudencia/scripts/atualizar_esteira.py",
    "skills/planejar-jurisprudencia/scripts/preparar_itens_esteira.py",
    "skills/comparar-materiais-enam/SKILL.md",
    "skills/comparar-materiais-enam/scripts/auditar_rastreabilidade.py",
    "skills/comparar-materiais-enam/modelos/manifesto-execucao.schema.json",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verifica a integração do plugin Magistratura e ENAM Brasil.")
    parser.add_argument("--plugin", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    raiz = args.plugin.resolve()
    erros: list[str] = []
    for relativo in ARQUIVOS_ESSENCIAIS:
        if not (raiz / relativo).is_file():
            erros.append(f"Arquivo essencial ausente: {relativo}")

    manifesto = raiz / ".codex-plugin" / "plugin.json"
    if manifesto.is_file():
        try:
            dados = json.loads(manifesto.read_text(encoding="utf-8"))
            if dados.get("name") != "magistratura-enam-br":
                erros.append("Manifesto com nome de plugin inesperado.")
            if dados.get("version") != "0.2.2":
                erros.append("Manifesto sem a versão consolidada 0.2.2.")
        except json.JSONDecodeError as exc:
            erros.append(f"Manifesto JSON inválido: {exc.msg}")

    for caminho in raiz.rglob("*.json"):
        try:
            json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            erros.append(f"JSON inválido em {caminho.relative_to(raiz)}: {exc}")
    for caminho in raiz.rglob("*.py"):
        try:
            py_compile.compile(str(caminho), doraise=True)
        except py_compile.PyCompileError as exc:
            erros.append(f"Python inválido em {caminho.relative_to(raiz)}: {exc.msg}")

    resultado = {
        "status": "aprovado" if not erros else "reprovado",
        "versao": "0.2.2",
        "checks": len(ARQUIVOS_ESSENCIAIS),
        "erros": erros,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if erros:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
