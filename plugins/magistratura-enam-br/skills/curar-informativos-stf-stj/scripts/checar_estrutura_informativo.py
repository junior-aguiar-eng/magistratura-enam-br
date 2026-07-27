#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PADRAO_CABECALHO = re.compile(r"\b(?:SUPREMO TRIBUNAL FEDERAL|SUPERIOR TRIBUNAL DE JUSTIÇA|INFORMATIVO)\b", re.I)
PADRAO_TITULO = re.compile(r"(?m)^\s*(?:\d{1,3}[.)-]|(?:RE|ARE|ADI|ADC|ADPF|ADO|HC|RHC|MS|RMS|REsp|AgInt|EAREsp)\b).{15,}$", re.I)


def ler_pdf(caminho: Path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Instale 'pypdf' antes de verificar o PDF.") from exc
    try:
        reader = PdfReader(str(caminho))
    except Exception as exc:
        raise RuntimeError(f"Não foi possível abrir o PDF: {exc}") from exc
    paginas = []
    for i, pagina in enumerate(reader.pages, 1):
        erro = ""
        try:
            texto = pagina.extract_text() or ""
        except Exception as exc:
            texto = ""
            erro = str(exc)
        paginas.append({"pagina": i, "texto": texto, "caracteres": len(texto.strip()), "erro_extracao": erro})
    return paginas


def analisar(paginas):
    total = len(paginas)
    caracteres = sum(int(p.get("caracteres", 0)) for p in paginas)
    vazias = [p["pagina"] for p in paginas if int(p.get("caracteres", 0)) == 0]
    curtas = [p["pagina"] for p in paginas if 0 < int(p.get("caracteres", 0)) < 120]
    erros = [p["pagina"] for p in paginas if p.get("erro_extracao")]
    texto = "\n".join(str(p.get("texto", "")) for p in paginas)
    cabecalho = bool(PADRAO_CABECALHO.search(texto))
    indicadores_titulo = len(PADRAO_TITULO.findall(texto))
    controles = sum(1 for c in texto if ord(c) < 32 and c not in "\n\r\t")
    substituicoes = texto.count("�")
    razao_corrupcao = (controles + substituicoes) / max(1, len(texto))

    avisos = []
    bloqueios = []
    if total == 0:
        bloqueios.append("PDF sem páginas.")
    if caracteres == 0:
        bloqueios.append("Nenhum texto foi extraído; o arquivo pode ser escaneado, protegido ou corrompido.")
    if total and len(vazias) / total >= 0.20:
        avisos.append("Ao menos 20% das páginas não possuem texto extraível; confira integridade e necessidade de OCR.")
    if curtas:
        avisos.append(f"Páginas com extração muito curta: {curtas}.")
    if erros:
        avisos.append(f"Páginas com erro de extração: {erros}.")
    if razao_corrupcao > 0.01:
        avisos.append("Há proporção relevante de caracteres de controle ou substituição; a extração pode estar corrompida.")
    if caracteres and not cabecalho:
        avisos.append("Cabeçalho institucional ou termo 'Informativo' não localizado.")
    if caracteres and indicadores_titulo == 0:
        avisos.append("Nenhum indicador de título foi localizado; confira manualmente a segmentação dos julgados.")

    status = "reprovado" if bloqueios else ("aprovado_com_ressalvas" if avisos else "aprovado")
    return {
        "status": status,
        "paginas": total,
        "caracteres_extraidos": caracteres,
        "paginas_sem_texto": vazias,
        "paginas_extracao_curta": curtas,
        "paginas_com_erro": erros,
        "cabecalho_detectado": cabecalho,
        "indicadores_de_titulo": indicadores_titulo,
        "razao_indicadores_corrupcao": round(razao_corrupcao, 6),
        "bloqueios": bloqueios,
        "avisos": avisos,
        "nota": "Os indicadores estruturais não constituem contagem definitiva de julgados e não substituem a leitura integral.",
    }


def main():
    parser = argparse.ArgumentParser(description="Verifica legibilidade e indicadores estruturais de informativo em PDF.")
    parser.add_argument("informativo", type=Path)
    parser.add_argument("--saida", type=Path)
    args = parser.parse_args()
    if not args.informativo.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.informativo}")
    try:
        resultado = analisar(ler_pdf(args.informativo))
    except RuntimeError as exc:
        raise SystemExit(f"ERRO: {exc}")
    conteudo = json.dumps(resultado, ensure_ascii=False, indent=2)
    print(conteudo)
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(conteudo, encoding="utf-8")
    raise SystemExit(2 if resultado["status"] == "reprovado" else 0)


if __name__ == "__main__":
    main()
