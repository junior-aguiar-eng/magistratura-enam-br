#!/usr/bin/env python3
"""Relatório local e descritivo de eventos de aprendizagem."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path

RESULTADOS_AVALIADOS = {"correto", "parcial", "incorreto"}


def _data_evento(evento: dict) -> date:
    valor = str(evento.get("occurred_at", ""))
    return datetime.fromisoformat(valor).date()


def _precisao(corretas: int, tentativas: int) -> float | None:
    return corretas / tentativas if tentativas else None


def gerar_relatorio(
    eventos: Iterable[dict], periodo: tuple[date, date]
) -> dict:
    """Agrega somente evidências observadas no período inclusivo informado."""
    inicio, fim = periodo
    if inicio > fim:
        raise ValueError("início do período deve ser anterior ou igual ao fim")

    selecionados = [
        evento for evento in eventos if inicio <= _data_evento(evento) <= fim
    ]
    tentativas = [
        evento
        for evento in selecionados
        if evento.get("activity", {}).get("attempt_observed") is True
        and evento.get("performance", {}).get("result") in RESULTADOS_AVALIADOS
    ]

    modalidades = defaultdict(lambda: {"tentativas": 0, "corretas": 0})
    erros = Counter()
    confianca = defaultdict(lambda: {"tentativas": 0, "corretas": 0})
    retencao = []

    for evento in tentativas:
        atividade = evento["activity"]
        desempenho = evento["performance"]
        resultado = desempenho["result"]
        modalidade = atividade["modality"]
        modalidades[modalidade]["tentativas"] += 1
        if resultado == "correto":
            modalidades[modalidade]["corretas"] += 1
        erros.update(desempenho.get("error_types", []))

        nivel_confianca = desempenho.get("confidence")
        if nivel_confianca is not None:
            confianca[nivel_confianca]["tentativas"] += 1
            if resultado == "correto":
                confianca[nivel_confianca]["corretas"] += 1

        if "retencao_revisao_posterior" in desempenho.get(
            "domain_evidence", []
        ):
            retencao.append(evento)

    precisao_modalidade = {}
    for modalidade, dados in sorted(modalidades.items()):
        precisao_modalidade[modalidade] = {
            **dados,
            "precisao": _precisao(dados["corretas"], dados["tentativas"]),
        }

    calibracao = {}
    for nivel, dados in sorted(confianca.items()):
        calibracao[nivel] = {
            **dados,
            "precisao": _precisao(dados["corretas"], dados["tentativas"]),
        }

    retencao_corretas = sum(
        evento["performance"]["result"] == "correto" for evento in retencao
    )
    if tentativas:
        estado = (
            "evidencia_disponivel"
            if any(
                evento["performance"]["result"] == "correto"
                for evento in tentativas
            )
            else "desempenho_insuficiente_observado"
        )
    else:
        estado = "sem_evidencia"

    return {
        "periodo": {"inicio": inicio.isoformat(), "fim": fim.isoformat()},
        "eventos_no_periodo": len(selecionados),
        "tentativas": len(tentativas),
        "estado_evidencia": estado,
        "precisao_por_modalidade": precisao_modalidade,
        "reincidencia_erros": {
            erro: quantidade
            for erro, quantidade in sorted(erros.items())
            if quantidade >= 2
        },
        "retencao_observada": {
            "evidencias": len(retencao),
            "sucessos": retencao_corretas,
            "precisao": _precisao(retencao_corretas, len(retencao)),
            "estado": "observada" if retencao else "sem_evidencia",
        },
        "calibracao_confianca": calibracao,
    }


def renderizar_markdown(relatorio: dict) -> str:
    """Renderiza o relatório já calculado sem acrescentar inferências."""
    linhas = [
        "# Relatório local de aprendizagem",
        "",
        f"Período: {relatorio['periodo']['inicio']} a {relatorio['periodo']['fim']}.",
        f"Tentativas observadas: {relatorio['tentativas']}.",
        f"Estado da evidência: `{relatorio['estado_evidencia']}`.",
        "",
        "## Precisão por modalidade",
    ]
    if not relatorio["precisao_por_modalidade"]:
        linhas.append("Sem evidência avaliativa no período.")
    for modalidade, dados in relatorio["precisao_por_modalidade"].items():
        precisao = dados["precisao"]
        percentual = "sem evidência" if precisao is None else f"{precisao:.1%}"
        linhas.append(
            f"- {modalidade}: {dados['corretas']}/{dados['tentativas']} ({percentual})"
        )
    linhas.extend(["", "## Reincidência de erros"])
    if not relatorio["reincidencia_erros"]:
        linhas.append("Nenhuma reincidência observada.")
    for erro, quantidade in relatorio["reincidencia_erros"].items():
        linhas.append(f"- {erro}: {quantidade}")
    linhas.extend(["", "## Retenção e confiança"])
    linhas.append(
        f"- Retenção: {relatorio['retencao_observada']['estado']}."
    )
    if not relatorio["calibracao_confianca"]:
        linhas.append("- Confiança: sem evidência declarada.")
    for nivel, dados in relatorio["calibracao_confianca"].items():
        linhas.append(
            f"- Confiança {nivel}: {dados['corretas']}/{dados['tentativas']} corretas."
        )
    return "\n".join(linhas) + "\n"


def _carregar_eventos(caminho: Path) -> list[dict]:
    texto = caminho.read_text(encoding="utf-8").strip()
    if not texto:
        return []
    if texto.startswith("["):
        dados = json.loads(texto)
    else:
        dados = [json.loads(linha) for linha in texto.splitlines() if linha.strip()]
    if not isinstance(dados, list) or not all(
        isinstance(evento, dict) for evento in dados
    ):
        raise ValueError("entrada deve conter uma lista JSON ou JSONL de eventos")
    return dados


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, required=True)
    parser.add_argument("--inicio", type=date.fromisoformat, required=True)
    parser.add_argument("--fim", type=date.fromisoformat, required=True)
    parser.add_argument("--formato", choices=("json", "markdown"), required=True)
    args = parser.parse_args()

    relatorio = gerar_relatorio(
        _carregar_eventos(args.entrada), (args.inicio, args.fim)
    )
    if args.formato == "json":
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    else:
        print(renderizar_markdown(relatorio), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
