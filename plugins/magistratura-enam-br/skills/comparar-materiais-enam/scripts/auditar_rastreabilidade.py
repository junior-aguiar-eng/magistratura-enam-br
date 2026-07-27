#!/usr/bin/env python3
"""Audita a rastreabilidade de um mapeamento e comparativo do ENAM.

O auditor verifica a estrutura mínima e os vínculos documentais declarados.
Ele não decide se a conclusão jurídica é correta nem substitui a leitura dos materiais.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TIPOS_EXPRESSOS = {
    "CORRESPONDENCIA EDITORIAL EXPRESSA",
    "DESLOCAMENTO EDITORIAL EXPRESSO",
}
CLASSIFICACOES = {
    "ATUALIZACAO LEGISLATIVA",
    "ATUALIZACAO JURISPRUDENCIAL",
    "ALTERACAO DOUTRINARIA MATERIAL",
    "CORRECAO DE CONTEUDO",
    "INCLUSAO MATERIAL",
    "EXCLUSAO MATERIAL CONFIRMADA",
    "SUPRESSAO APARENTE - REVISAO HUMANA",
    "SEM DELTA",
    "PENDENTE DE PUBLICACAO",
    "AMBIGUO - REVISAO HUMANA",
}


def texto(valor) -> str:
    return "" if valor is None else str(valor).strip()


def carregar(caminho: Path):
    if not caminho.exists():
        raise ValueError(f"Arquivo não encontrado: {caminho}")
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido em {caminho.name}: {exc.msg}") from exc


def refs_validas(refs, caminho: str, documentos: set[str], erros: list[str], exigir: bool = False) -> None:
    if not isinstance(refs, list):
        erros.append(f"{caminho}: referências devem ser uma lista.")
        return
    if exigir and not refs:
        erros.append(f"{caminho}: exige ao menos uma referência.")
    for indice, referencia in enumerate(refs, start=1):
        prefixo = f"{caminho}[{indice}]"
        if not isinstance(referencia, dict):
            erros.append(f"{prefixo}: referência inválida.")
            continue
        documento = texto(referencia.get("documento"))
        pagina = texto(referencia.get("pagina"))
        localizacao = texto(referencia.get("localizacao"))
        if not documento or documento not in documentos:
            erros.append(f"{prefixo}: documento não consta do manifesto.")
        if not pagina:
            erros.append(f"{prefixo}: página não informada.")
        if not localizacao:
            erros.append(f"{prefixo}: localização não informada.")


def auditar_manifesto(manifesto, erros: list[str]) -> set[str]:
    if not isinstance(manifesto, dict) or not texto(manifesto.get("escopo")):
        erros.append("manifesto: escopo obrigatório ausente.")
        return set()
    documentos = manifesto.get("documentos")
    if not isinstance(documentos, list) or len(documentos) < 2:
        erros.append("manifesto: informe ao menos dois documentos identificados.")
        return set()
    ids = set()
    for indice, documento in enumerate(documentos, start=1):
        prefixo = f"manifesto.documentos[{indice}]"
        if not isinstance(documento, dict):
            erros.append(f"{prefixo}: registro inválido.")
            continue
        identificador = texto(documento.get("id"))
        if not identificador:
            erros.append(f"{prefixo}: id obrigatório ausente.")
        elif identificador in ids:
            erros.append(f"{prefixo}: id de documento duplicado.")
        else:
            ids.add(identificador)
        for campo in ("edicao", "arquivo", "tipo_fonte"):
            if not texto(documento.get(campo)):
                erros.append(f"{prefixo}: {campo} obrigatório ausente.")
    return ids


def auditar_mapeamento(mapeamento, documentos: set[str], erros: list[str]) -> None:
    if not isinstance(mapeamento, dict) or not texto(mapeamento.get("escopo")):
        erros.append("mapeamento: escopo obrigatório ausente.")
        return
    itens = mapeamento.get("itens")
    if not isinstance(itens, list):
        erros.append("mapeamento: itens devem ser uma lista.")
        return
    for indice, item in enumerate(itens, start=1):
        prefixo = f"mapeamento.itens[{indice}]"
        if not isinstance(item, dict):
            erros.append(f"{prefixo}: item inválido.")
            continue
        for campo in ("disciplina", "tema_subtema", "tipo_correspondencia"):
            if not texto(item.get(campo)):
                erros.append(f"{prefixo}: {campo} obrigatório ausente.")
        tipo = texto(item.get("tipo_correspondencia"))
        if tipo in TIPOS_EXPRESSOS and not texto(item.get("base_editorial")):
            erros.append(f"{prefixo}: correspondência expressa exige base_editorial.")
        refs_validas(item.get("referencias_anteriores"), f"{prefixo}.referencias_anteriores", documentos, erros)
        refs_validas(item.get("referencias_atuais"), f"{prefixo}.referencias_atuais", documentos, erros)
        refs_validas(item.get("evidencias"), f"{prefixo}.evidencias", documentos, erros, exigir=True)


def auditar_comparativo(comparativo, documentos: set[str], erros: list[str]) -> None:
    if not isinstance(comparativo, dict) or not texto(comparativo.get("escopo")):
        erros.append("comparativo: escopo obrigatório ausente.")
        return
    itens = comparativo.get("itens")
    if not isinstance(itens, list):
        erros.append("comparativo: itens devem ser uma lista.")
        return
    for indice, item in enumerate(itens, start=1):
        prefixo = f"comparativo.itens[{indice}]"
        if not isinstance(item, dict):
            erros.append(f"{prefixo}: item inválido.")
            continue
        for campo in ("disciplina", "tema_subtema", "tipo_correspondencia", "classificacao", "delta_real"):
            if not texto(item.get(campo)):
                erros.append(f"{prefixo}: {campo} obrigatório ausente.")
        classificacao = texto(item.get("classificacao"))
        if classificacao and classificacao not in CLASSIFICACOES:
            erros.append(f"{prefixo}: classificação não padronizada.")
        refs_anteriores = item.get("referencias_anteriores")
        refs_atuais = item.get("referencias_atuais")
        refs_validas(refs_anteriores, f"{prefixo}.referencias_anteriores", documentos, erros)
        refs_validas(refs_atuais, f"{prefixo}.referencias_atuais", documentos, erros)
        refs_validas(item.get("evidencias"), f"{prefixo}.evidencias", documentos, erros, exigir=True)
        if classificacao == "EXCLUSAO MATERIAL CONFIRMADA":
            refs_validas(refs_anteriores, f"{prefixo}.referencias_anteriores", documentos, erros, exigir=True)
            refs_validas(refs_atuais, f"{prefixo}.referencias_atuais", documentos, erros, exigir=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audita rastreabilidade de comparação ENAM.")
    parser.add_argument("--manifesto", required=True, type=Path)
    parser.add_argument("--mapeamento", required=True, type=Path)
    parser.add_argument("--comparativo", required=True, type=Path)
    args = parser.parse_args()
    erros: list[str] = []
    try:
        manifesto = carregar(args.manifesto)
        mapeamento = carregar(args.mapeamento)
        comparativo = carregar(args.comparativo)
    except ValueError as exc:
        raise SystemExit(f"ERRO: {exc}")
    documentos = auditar_manifesto(manifesto, erros)
    auditar_mapeamento(mapeamento, documentos, erros)
    auditar_comparativo(comparativo, documentos, erros)
    resultado = {"status": "aprovado" if not erros else "reprovado", "erros": erros}
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if erros:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
