#!/usr/bin/env python3
"""Verifica a integridade estrutural do plugin sem escrever na árvore auditada."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tomllib


ARQUIVOS_ESSENCIAIS = (
    ".codex-plugin/plugin.json",
    "AGENTS.md",
    "pyproject.toml",
    ".python-version",
    "uv.lock",
    "requirements.txt",
    "references/protocolo-uso-do-acervo.md",
    "skills/curar-informativos-stf-stj/SKILL.md",
    "skills/curar-informativos-stf-stj/modelos/precedentes.schema.json",
    "skills/curar-informativos-stf-stj/scripts/atualizar_planilha_precedentes.py",
    "skills/estudar-direito-magistratura/SKILL.md",
    "skills/planejar-jurisprudencia/SKILL.md",
    "skills/planejar-jurisprudencia/scripts/atualizar_esteira.py",
    "skills/planejar-jurisprudencia/scripts/preparar_itens_esteira.py",
    "skills/comparar-materiais-enam/SKILL.md",
    "skills/comparar-materiais-enam/references/formato-entrega-comparativo.md",
    "skills/comparar-materiais-enam/scripts/auditar_rastreabilidade.py",
    "skills/comparar-materiais-enam/modelos/manifesto-execucao.schema.json",
)

DIRETORIOS_GERADOS = frozenset({
    ".git",
    ".pytest_cache",
    ".test-deps",
    ".test-tmp",
    ".venv",
    ".venv-test-curadoria",
    "__pycache__",
    "build",
    "dist",
})


def arquivos_fonte(raiz: Path, padrao: str):
    """Percorre somente arquivos distribuíveis, sem caches ou ambientes locais."""
    for caminho in raiz.rglob(padrao):
        relativo = caminho.relative_to(raiz)
        if not any(parte in DIRETORIOS_GERADOS for parte in relativo.parts):
            yield caminho


def validar_ambiente_uv(raiz: Path, erros: list[str]) -> None:
    """Confirma o contrato do ambiente sem sincronizar ou alterar arquivos."""
    pyproject = raiz / "pyproject.toml"
    python_version = raiz / ".python-version"
    lock = raiz / "uv.lock"
    if pyproject.is_file():
        try:
            projeto = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
            if projeto.get("name") != "magistratura-enam-br":
                erros.append("pyproject.toml com nome de projeto inesperado.")
            if projeto.get("requires-python") != ">=3.13,<3.14":
                erros.append("pyproject.toml deve fixar compatibilidade em Python 3.13.")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            erros.append(f"pyproject.toml inválido: {exc}")
    if python_version.is_file() and python_version.read_text(encoding="utf-8").strip() != "3.13":
        erros.append(".python-version deve fixar Python 3.13.")
    if lock.is_file():
        try:
            dados_lock = tomllib.loads(lock.read_text(encoding="utf-8"))
            if dados_lock.get("requires-python") != "==3.13.*":
                erros.append("uv.lock deve estar resolvido para Python 3.13.")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            erros.append(f"uv.lock inválido: {exc}")

    uv = shutil.which("uv")
    if not uv:
        erros.append("uv não encontrado para validar uv.lock.")
        return
    resultado = subprocess.run(
        [uv, "lock", "--check"],
        cwd=raiz,
        capture_output=True,
        text=True,
        check=False,
    )
    if resultado.returncode:
        detalhe = (resultado.stderr or resultado.stdout).strip()
        erros.append(f"uv.lock não está sincronizado com pyproject.toml: {detalhe or 'uv lock --check falhou.'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verifica a integração do plugin Magistratura e ENAM Brasil.")
    parser.add_argument("--plugin", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    raiz = args.plugin.resolve()
    erros: list[str] = []
    for relativo in ARQUIVOS_ESSENCIAIS:
        if not (raiz / relativo).is_file():
            erros.append(f"Arquivo essencial ausente: {relativo}")

    validar_ambiente_uv(raiz, erros)

    manifesto = raiz / ".codex-plugin" / "plugin.json"
    versao = None
    if manifesto.is_file():
        try:
            dados = json.loads(manifesto.read_text(encoding="utf-8"))
            if dados.get("name") != "magistratura-enam-br":
                erros.append("Manifesto com nome de plugin inesperado.")
            versao = dados.get("version")
            if not isinstance(versao, str) or not versao.strip():
                erros.append("Manifesto sem versão não vazia.")
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            erros.append(f"Manifesto JSON inválido: {exc}")

    total_json = 0
    for caminho in arquivos_fonte(raiz, "*.json"):
        total_json += 1
        try:
            json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            erros.append(f"JSON inválido em {caminho.relative_to(raiz)}: {exc}")
    total_python = 0
    for caminho in arquivos_fonte(raiz, "*.py"):
        total_python += 1
        try:
            compile(caminho.read_text(encoding="utf-8"), str(caminho), "exec")
        except (OSError, UnicodeError, SyntaxError) as exc:
            erros.append(f"Python inválido em {caminho.relative_to(raiz)}: {exc}")

    resultado = {
        "status": "aprovado" if not erros else "reprovado",
        "versao": versao,
        "checks": len(ARQUIVOS_ESSENCIAIS),
        "arquivos_json": total_json,
        "arquivos_python": total_python,
        "erros": erros,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if erros:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
