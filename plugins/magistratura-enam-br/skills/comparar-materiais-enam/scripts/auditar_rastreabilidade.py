#!/usr/bin/env python3
"""Audita a rastreabilidade de um mapeamento e comparativo do ENAM.

O auditor verifica a estrutura mínima e os vínculos documentais declarados.
Ele não decide se a conclusão jurídica é correta nem substitui a leitura dos materiais.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

TIPOS_EXPRESSOS = {
    "CORRESPONDENCIA EDITORIAL EXPRESSA",
    "DESLOCAMENTO EDITORIAL EXPRESSO",
}
TIPOS_CORRESPONDENCIA = {
    *TIPOS_EXPRESSOS,
    "CORRESPONDENCIA TEMATICA CONFIRMADA",
    "CORRESPONDENCIA PARCIAL",
    "CORRESPONDENCIA TEMATICA PROVAVEL",
    "CORRESPONDENCIA NAO CONFIRMADA",
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
CLASSIFICACOES_COM_REFERENCIAS_BILATERAIS = CLASSIFICACOES - {"PENDENTE DE PUBLICACAO"}
FUNDAMENTOS_POR_CLASSIFICACAO = {
    "ATUALIZACAO LEGISLATIVA": "LEGISLACAO",
    "ATUALIZACAO JURISPRUDENCIAL": "JURISPRUDENCIA",
}
ACOES_POR_CLASSIFICACAO = {
    "ATUALIZACAO LEGISLATIVA": "SUBSTITUIR",
    "ATUALIZACAO JURISPRUDENCIAL": "SUBSTITUIR",
    "ALTERACAO DOUTRINARIA MATERIAL": "SUBSTITUIR",
    "CORRECAO DE CONTEUDO": "SUBSTITUIR",
    "INCLUSAO MATERIAL": "INCLUIR",
    "EXCLUSAO MATERIAL CONFIRMADA": "SUBSTITUIR",
    "SUPRESSAO APARENTE - REVISAO HUMANA": "REVISAR",
    "SEM DELTA": "SEM_ACAO",
    "PENDENTE DE PUBLICACAO": "AGUARDAR_PUBLICACAO",
    "AMBIGUO - REVISAO HUMANA": "REVISAR",
}
RAIZ_SKILL = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "manifesto": RAIZ_SKILL / "modelos" / "manifesto-execucao.schema.json",
    "mapeamento": RAIZ_SKILL / "modelos" / "mapeamento.schema.json",
    "comparativo": RAIZ_SKILL / "modelos" / "comparativo.schema.json",
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


def validar_schema(nome: str, dados, erros: list[str]) -> None:
    """Aplica o schema publicado antes das verificações semânticas próprias."""
    try:
        schema = json.loads(SCHEMAS[nome].read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        erros.append(f"{nome}: schema indisponível ou inválido: {exc}")
        return
    validador = Draft202012Validator(schema)
    for erro in sorted(validador.iter_errors(dados), key=lambda item: list(item.absolute_path)):
        caminho = ".".join(str(parte) for parte in erro.absolute_path) or "raiz"
        erros.append(f"{nome}: schema inválido em {caminho}: {erro.message}")


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


def auditar_execucao(manifesto, mapeamento, comparativo, erros: list[str]) -> None:
    identificador = texto(manifesto.get("id_execucao")) if isinstance(manifesto, dict) else ""
    escopo = texto(manifesto.get("escopo")) if isinstance(manifesto, dict) else ""
    for nome, artefato in (("mapeamento", mapeamento), ("comparativo", comparativo)):
        atual = texto(artefato.get("id_execucao")) if isinstance(artefato, dict) else ""
        escopo_atual = texto(artefato.get("escopo")) if isinstance(artefato, dict) else ""
        if identificador and atual and atual != identificador:
            erros.append(f"{nome}: id_execucao diverge do manifesto.")
        if escopo and escopo_atual and escopo_atual != escopo:
            erros.append(f"{nome}: escopo diverge do manifesto.")


def auditar_mapeamento(mapeamento, documentos: set[str], erros: list[str]) -> dict[str, dict[str, str]]:
    if not isinstance(mapeamento, dict) or not texto(mapeamento.get("escopo")):
        erros.append("mapeamento: escopo obrigatório ausente.")
        return {}
    itens = mapeamento.get("itens")
    if not isinstance(itens, list):
        erros.append("mapeamento: itens devem ser uma lista.")
        return {}
    itens_por_id: dict[str, dict[str, str]] = {}
    for indice, item in enumerate(itens, start=1):
        prefixo = f"mapeamento.itens[{indice}]"
        if not isinstance(item, dict):
            erros.append(f"{prefixo}: item inválido.")
            continue
        for campo in ("id_item", "disciplina", "tema_subtema", "tipo_correspondencia"):
            if not texto(item.get(campo)):
                erros.append(f"{prefixo}: {campo} obrigatório ausente.")
        identificador = texto(item.get("id_item"))
        if identificador and identificador in itens_por_id:
            erros.append(f"{prefixo}: id_item duplicado: {identificador}.")
        tipo = texto(item.get("tipo_correspondencia"))
        if tipo and tipo not in TIPOS_CORRESPONDENCIA:
            erros.append(f"{prefixo}: tipo_correspondencia não padronizado.")
        if identificador and identificador not in itens_por_id:
            itens_por_id[identificador] = {
                "tipo_correspondencia": tipo,
                "disciplina": texto(item.get("disciplina")),
                "tema_subtema": texto(item.get("tema_subtema")),
            }
        if tipo in TIPOS_EXPRESSOS and not texto(item.get("base_editorial")):
            erros.append(f"{prefixo}: correspondência expressa exige base_editorial.")
        refs_validas(item.get("referencias_anteriores"), f"{prefixo}.referencias_anteriores", documentos, erros)
        refs_validas(item.get("referencias_atuais"), f"{prefixo}.referencias_atuais", documentos, erros)
        refs_validas(item.get("evidencias"), f"{prefixo}.evidencias", documentos, erros, exigir=True)
    return itens_por_id


def auditar_comparativo(comparativo, documentos: set[str], itens_por_id: dict[str, dict[str, str]], erros: list[str]) -> None:
    if not isinstance(comparativo, dict) or not texto(comparativo.get("escopo")):
        erros.append("comparativo: escopo obrigatório ausente.")
        return
    itens = comparativo.get("itens")
    if not isinstance(itens, list):
        erros.append("comparativo: itens devem ser uma lista.")
        return
    itens_referenciados: set[str] = set()
    classificacoes_por_item: dict[str, list[str]] = {}
    for indice, item in enumerate(itens, start=1):
        prefixo = f"comparativo.itens[{indice}]"
        if not isinstance(item, dict):
            erros.append(f"{prefixo}: item inválido.")
            continue
        for campo in ("id_item", "disciplina", "tema_subtema", "tipo_correspondencia", "classificacao", "delta_real"):
            if not texto(item.get(campo)):
                erros.append(f"{prefixo}: {campo} obrigatório ausente.")
        identificador = texto(item.get("id_item"))
        classificacao = texto(item.get("classificacao"))
        acao_recomendada = texto(item.get("acao_recomendada"))
        tipo = texto(item.get("tipo_correspondencia"))
        if tipo and tipo not in TIPOS_CORRESPONDENCIA:
            erros.append(f"{prefixo}: tipo_correspondencia não padronizado.")
        item_mapeado = itens_por_id.get(identificador)
        if identificador and item_mapeado is None:
            erros.append(f"{prefixo}: id_item não existe no mapeamento: {identificador}.")
        elif identificador:
            itens_referenciados.add(identificador)
            classificacoes_por_item.setdefault(identificador, []).append(classificacao)
            if tipo and tipo != item_mapeado["tipo_correspondencia"]:
                erros.append(f"{prefixo}: tipo_correspondencia diverge do mapeamento para {identificador}.")
            for campo in ("disciplina", "tema_subtema"):
                if texto(item.get(campo)) != item_mapeado[campo]:
                    erros.append(f"{prefixo}: {campo} diverge do mapeamento para {identificador}.")
        if classificacao and classificacao not in CLASSIFICACOES:
            erros.append(f"{prefixo}: classificação não padronizada.")
        acao_esperada = ACOES_POR_CLASSIFICACAO.get(classificacao)
        if acao_esperada and acao_recomendada != acao_esperada:
            erros.append(f"{prefixo}: acao_recomendada deve ser {acao_esperada} para {classificacao}.")
        refs_anteriores = item.get("referencias_anteriores")
        refs_atuais = item.get("referencias_atuais")
        exigir_referencias_bilaterais = classificacao in CLASSIFICACOES_COM_REFERENCIAS_BILATERAIS
        refs_validas(refs_anteriores, f"{prefixo}.referencias_anteriores", documentos, erros, exigir=exigir_referencias_bilaterais)
        refs_validas(refs_atuais, f"{prefixo}.referencias_atuais", documentos, erros, exigir=exigir_referencias_bilaterais)
        refs_validas(item.get("evidencias"), f"{prefixo}.evidencias", documentos, erros, exigir=True)
        tipo_fundamento = FUNDAMENTOS_POR_CLASSIFICACAO.get(classificacao)
        if tipo_fundamento:
            fundamento = item.get("fundamento_material")
            if not isinstance(fundamento, dict):
                erros.append(f"{prefixo}: {classificacao} exige fundamento_material oficial.")
            else:
                if texto(fundamento.get("tipo")) != tipo_fundamento:
                    erros.append(f"{prefixo}: fundamento_material.tipo deve ser {tipo_fundamento}.")
                for campo in ("identificador", "fonte_oficial"):
                    if not texto(fundamento.get(campo)):
                        erros.append(f"{prefixo}: fundamento_material.{campo} obrigatÃ³rio ausente.")
    for identificador, classificacoes in classificacoes_por_item.items():
        if "SEM DELTA" in classificacoes and len(classificacoes) > 1:
            erros.append(f"comparativo: SEM DELTA deve ser exclusivo para {identificador}.")
    sem_comparativo = sorted(set(itens_por_id).difference(itens_referenciados))
    if sem_comparativo:
        erros.append(f"comparativo: id_item sem delta correspondente: {', '.join(sem_comparativo)}.")


def auditar(manifesto, mapeamento, comparativo) -> list[str]:
    erros: list[str] = []
    validar_schema("manifesto", manifesto, erros)
    validar_schema("mapeamento", mapeamento, erros)
    validar_schema("comparativo", comparativo, erros)
    auditar_execucao(manifesto, mapeamento, comparativo, erros)
    documentos = auditar_manifesto(manifesto, erros)
    itens_por_id = auditar_mapeamento(mapeamento, documentos, erros)
    auditar_comparativo(comparativo, documentos, itens_por_id, erros)
    return erros


def main() -> None:
    parser = argparse.ArgumentParser(description="Audita rastreabilidade de comparação ENAM.")
    parser.add_argument("--manifesto", required=True, type=Path)
    parser.add_argument("--mapeamento", required=True, type=Path)
    parser.add_argument("--comparativo", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifesto = carregar(args.manifesto)
        mapeamento = carregar(args.mapeamento)
        comparativo = carregar(args.comparativo)
    except ValueError as exc:
        raise SystemExit(f"ERRO: {exc}")
    erros = auditar(manifesto, mapeamento, comparativo)
    resultado = {"status": "aprovado" if not erros else "reprovado", "erros": erros}
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if erros:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
