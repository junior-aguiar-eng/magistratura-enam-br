#!/usr/bin/env python3
"""Calcula recomendação adaptativa sem substituir a política fixa por padrão."""

from __future__ import annotations

import datetime as dt
import math


def _data_iso(valor: str) -> dt.date:
    try:
        return dt.datetime.fromisoformat(valor).date()
    except (AttributeError, ValueError) as exc:
        raise ValueError("occurred_at inválido") from exc


def recomendar_revisao(evento: dict, intervalo_fixo: int, modo_sombra: bool = True) -> dict:
    """Aplica a política v1 e preserva o intervalo fixo no modo sombra."""
    if isinstance(intervalo_fixo, bool) or not isinstance(intervalo_fixo, int) or not 1 <= intervalo_fixo <= 90:
        raise ValueError("intervalo_fixo deve ser inteiro entre 1 e 90")
    desempenho = evento.get("performance")
    if not isinstance(desempenho, dict):
        raise TypeError("performance ausente")
    for campo in ("result", "confidence", "domain_evidence"):
        if campo not in desempenho:
            raise ValueError(f"{campo} ausente")
    resultado = desempenho["result"]
    confianca = desempenho["confidence"]
    evidencias = desempenho["domain_evidence"]
    if resultado not in {"correto", "parcial", "incorreto"}:
        raise ValueError("result não permite recomendação")
    if confianca not in {None, "baixa", "media", "alta"}:
        raise ValueError("confidence inválida")
    if not isinstance(evidencias, list):
        raise TypeError("domain_evidence deve ser lista")
    motivos_evento = evento.get("routing", {}).get("reason_codes", [])
    fundamentou = "fundamentacao_normativa_jurisprudencial" in evidencias
    transferiu = "aplicacao_fatos_novos" in evidencias

    if "repeated_error" in motivos_evento:
        sugerido, motivo = 1, "repeated_error"
    elif resultado == "incorreto":
        sugerido, motivo = 1, "incorrect"
    elif resultado == "parcial":
        sugerido, motivo = min(3, intervalo_fixo), "partial"
    elif confianca == "baixa":
        sugerido, motivo = intervalo_fixo, "low_confidence"
    elif confianca != "alta":
        sugerido, motivo = intervalo_fixo, "fixed_policy_preserved"
    elif not fundamentou:
        sugerido, motivo = intervalo_fixo, "missing_justification"
    elif transferiu:
        sugerido, motivo = min(90, math.floor(intervalo_fixo * 1.5)), "high_confidence_with_transfer"
    else:
        sugerido, motivo = math.floor(intervalo_fixo * 1.25), "high_confidence_no_transfer"

    data = _data_iso(evento.get("occurred_at"))
    fixa = data + dt.timedelta(days=intervalo_fixo)
    sugestao = data + dt.timedelta(days=sugerido)
    efetiva = fixa if modo_sombra else sugestao
    return {
        "schema_version": "1.0.0",
        "policy": "adaptive_v1",
        "base_interval_days": intervalo_fixo,
        "suggested_interval_days": sugerido,
        "reason_codes": [motivo],
        "shadow_mode": modo_sombra,
        "fixed_review_at": fixa.isoformat(),
        "suggested_review_at": sugestao.isoformat(),
        "effective_review_at": efetiva.isoformat(),
    }
