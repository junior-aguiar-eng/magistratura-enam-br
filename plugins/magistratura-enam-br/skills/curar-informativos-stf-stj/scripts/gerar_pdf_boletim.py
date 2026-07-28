#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from common import CONFIANCAS, ESTADOS, texto, validar_data_iso, validar_schema


def validar_julgado(julgado, contexto):
    if not isinstance(julgado, dict):
        raise ValueError(f"{contexto} deve ser objeto.")
    for campo in ("titulo", "comentario", "estado_jurisprudencial", "grau_confianca", "data_verificacao"):
        if not texto(julgado.get(campo)):
            raise ValueError(f"{contexto}: campo obrigatório ausente: {campo}.")
    estado = texto(julgado["estado_jurisprudencial"]).lower()
    confianca = texto(julgado["grau_confianca"]).lower()
    if estado not in ESTADOS:
        raise ValueError(f"{contexto}: estado jurisprudencial inválido: {estado}.")
    if confianca not in CONFIANCAS:
        raise ValueError(f"{contexto}: grau de confiança inválido: {confianca}.")
    validar_data_iso(julgado["data_verificacao"], "data_verificacao", contexto)
    if (estado != "confirmado" or confianca != "alto") and not texto(julgado.get("nota_estado")):
        raise ValueError(f"{contexto}: 'nota_estado' é obrigatória diante de ressalva ou confiança inferior a alta.")
    fontes = julgado.get("fontes_essenciais", [])
    if fontes is not None and not isinstance(fontes, list):
        raise ValueError(f"{contexto}: 'fontes_essenciais' deve ser lista.")


def validar_dados(dados):
    validar_schema("boletim.schema.json", dados)
    if not isinstance(dados, dict):
        raise ValueError("A raiz do JSON deve ser objeto.")
    for campo in ("titulo_boletim", "data_geracao", "nota_metodologica"):
        if not texto(dados.get(campo)):
            raise ValueError(f"Campo obrigatório ausente: {campo}.")
    validar_data_iso(dados["data_geracao"], "data_geracao")
    for chave in ("julgados_stf", "julgados_stj"):
        lista = dados.get(chave)
        if not isinstance(lista, list):
            raise ValueError(f"'{chave}' deve ser lista.")
        for i, julgado in enumerate(lista, 1):
            validar_julgado(julgado, f"{chave}[{i}]")
    for chave in ("nao_selecionados", "pendencias", "fontes_essenciais"):
        valor = dados.get(chave, [])
        if not isinstance(valor, list):
            raise ValueError(f"'{chave}' deve ser lista.")
    return dados


def imports_reportlab():
    try:
        from reportlab.lib.enums import TA_JUSTIFY
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        raise RuntimeError("Instale 'reportlab' antes de gerar o PDF.") from exc
    return locals()


def seguro(value):
    return escape(texto(value))


def paragrafos(value):
    return [seguro(p).replace("\n", "<br/>") for p in str(value or "").split("\n\n") if p.strip()]


def gerar(dados, saida):
    r = imports_reportlab()
    styles = r["getSampleStyleSheet"]()
    PS = r["ParagraphStyle"]
    estilos = {
        "titulo": PS("Titulo", parent=styles["Title"], fontName="Times-Bold", fontSize=18, leading=22, alignment=1, spaceAfter=7),
        "sub": PS("Sub", parent=styles["Normal"], fontName="Times-Italic", fontSize=9.5, leading=12, alignment=1, spaceAfter=16),
        "secao": PS("Secao", parent=styles["Heading1"], fontName="Times-Bold", fontSize=14, leading=18, spaceBefore=16, spaceAfter=9),
        "julgado": PS("Julgado", parent=styles["Heading2"], fontName="Times-Bold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=5),
        "etiqueta": PS("Etiqueta", parent=styles["Normal"], fontName="Times-Bold", fontSize=8.5, leading=11, spaceAfter=7),
        "corpo": PS("Corpo", parent=styles["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=15, alignment=r["TA_JUSTIFY"], spaceAfter=8),
    }
    doc = r["SimpleDocTemplate"](
        str(saida), pagesize=r["A4"], leftMargin=2.4*r["cm"], rightMargin=2.4*r["cm"],
        topMargin=2.2*r["cm"], bottomMargin=2.2*r["cm"],
        title=texto(dados["titulo_boletim"]), author="Curadoria de Informativos",
    )
    story = [r["Paragraph"](seguro(dados["titulo_boletim"]), estilos["titulo"])]
    story.append(r["Paragraph"](seguro(f"Gerado em {dados['data_geracao']}"), estilos["sub"]))
    story.append(r["Paragraph"]("Nota metodológica", estilos["secao"]))
    for p in paragrafos(dados["nota_metodologica"]):
        story.append(r["Paragraph"](p, estilos["corpo"]))

    for chave, rotulo in (("julgados_stf", "Julgados do STF"), ("julgados_stj", "Julgados do STJ")):
        if not dados[chave]:
            continue
        story.append(r["Paragraph"](rotulo, estilos["secao"]))
        for julgado in dados[chave]:
            story.append(r["Paragraph"](seguro(julgado["titulo"]), estilos["julgado"]))
            etiqueta = (
                f"Estado jurisprudencial: {julgado['estado_jurisprudencial']} | "
                f"Confiança: {julgado['grau_confianca']} | Verificado em: {julgado['data_verificacao']}"
            )
            story.append(r["Paragraph"](seguro(etiqueta), estilos["etiqueta"]))
            if texto(julgado.get("nota_estado")):
                story.append(r["Paragraph"](seguro("Ressalva: " + texto(julgado["nota_estado"])), estilos["corpo"]))
            for p in paragrafos(julgado["comentario"]):
                story.append(r["Paragraph"](p, estilos["corpo"]))
            story.append(r["Spacer"](1, 0.2*r["cm"]))

    secoes = [
        ("nao_selecionados", "Julgados relevantes não selecionados"),
        ("pendencias", "Pendências e ressalvas editoriais"),
        ("fontes_essenciais", "Fontes essenciais"),
    ]
    for chave, rotulo in secoes:
        itens = dados.get(chave, [])
        if not itens:
            continue
        story.append(r["Paragraph"](rotulo, estilos["secao"]))
        for item in itens:
            story.append(r["Paragraph"](seguro("• " + texto(item)), estilos["corpo"]))

    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)


def main():
    parser = argparse.ArgumentParser(description="Gera PDF do boletim a partir de JSON validado.")
    parser.add_argument("entrada", type=Path)
    parser.add_argument("saida", type=Path)
    args = parser.parse_args()
    if not args.entrada.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.entrada}")
    try:
        dados = validar_dados(json.loads(args.entrada.read_text(encoding="utf-8")))
        gerar(dados, args.saida)
    except (json.JSONDecodeError, ValueError, RuntimeError) as exc:
        raise SystemExit(f"ERRO: {exc}")
    print(args.saida)


if __name__ == "__main__":
    main()
