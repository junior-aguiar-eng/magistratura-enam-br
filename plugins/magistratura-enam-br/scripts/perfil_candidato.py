#!/usr/bin/env python3
"""Projeção reconstruível do perfil pedagógico."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

from eventos_aprendizagem import ler_eventos, validar_evento
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "modelos/pedagogia/candidate-profile.schema.json"
SETTINGS_SCHEMA = ROOT / "modelos/pedagogia/profile-settings.schema.json"
EVIDENCIAS = ("evocacao_regra", "discriminacao_institutos", "aplicacao_fatos_novos", "fundamentacao_normativa_jurisprudencial", "expressao_objetiva_discursiva_oral", "retencao_revisao_posterior")


def _identificador_conteudo(evento: dict) -> str:
    referencia = evento["content_ref"]
    return referencia.get("id") or referencia["content_id"]


def _chave(evento: dict) -> str:
    return f"{_identificador_conteudo(evento)}--{evento['activity']['modality'].replace('_', '-')}"


def _nivel_evidencia(evento: dict) -> str:
    assistencia = evento["activity"].get("assistance_level", "nao_registrada")
    if evento["performance"]["result"] != "correto":
        return "em_desenvolvimento"
    if assistencia in {"nao_registrada", "nenhuma", "pista"}:
        return "demonstrado"
    return "em_desenvolvimento"


def _configuracao_validada(configuracao: dict | None) -> dict:
    declarada = configuracao or {"schema_version": "1.0.0", "objectives": [], "preferences": {}}
    schema = json.loads(SETTINGS_SCHEMA.read_text(encoding="utf-8"))
    erros = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(declarada))
    if erros:
        raise ValueError(f"Configuração inválida: {erros[0].message}")
    return declarada


def reconstruir_perfil(eventos: Iterable[dict], configuracao: dict | None = None) -> dict:
    ordenados = sorted(eventos, key=lambda e: (e.get("occurred_at", ""), e.get("event_id", "")))
    ids, competencias, remediacoes = set(), {}, {}
    for evento in ordenados:
        erros = validar_evento(evento)
        if erros:
            raise ValueError(f"Evento inválido: {'; '.join(erros)}")
        event_id = evento["event_id"]
        if event_id in ids:
            raise ValueError(f"event_id duplicado: {event_id}")
        ids.add(event_id)
        if not evento["activity"]["attempt_observed"]:
            continue
        chave = _chave(evento)
        item = competencias.setdefault(chave, {"competency_id": chave, "evidence": {e: "nao_observado" for e in EVIDENCIAS}, "observations": []})
        desempenho = evento["performance"]
        item["observations"].append({"event_id": event_id, "occurred_at": evento["occurred_at"], "result": desempenho["result"], "error_types": desempenho["error_types"], "domain_evidence": desempenho["domain_evidence"], "confidence": desempenho["confidence"], "assistance_level": evento["activity"].get("assistance_level", "nao_registrada")})
        nivel = _nivel_evidencia(evento)
        for evidencia in desempenho["domain_evidence"]:
            item["evidence"][evidencia] = nivel
        if desempenho["result"] in {"parcial", "incorreto"} and desempenho["error_types"]:
            remediacoes[chave] = {"remediation_id": event_id.replace("evt_", "rem_", 1), "competency_id": chave, "error_types": desempenho["error_types"], "opened_by_event_id": event_id}
        elif desempenho["result"] == "correto" and nivel == "demonstrado":
            remediacoes.pop(chave, None)
    return {"schema_version": "2.0.0", "updated_at": ordenados[-1]["occurred_at"] if ordenados else "1970-01-01T00:00:00Z", "declared": _configuracao_validada(configuracao), "competencies": [competencias[k] for k in sorted(competencias)], "open_remediations": [remediacoes[k] for k in sorted(remediacoes)]}


def salvar_perfil_atomico(caminho: Path, perfil: dict) -> None:
    caminho = Path(caminho)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    erros = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(perfil))
    if erros:
        raise ValueError(f"Perfil inválido: {erros[0].message}")
    if not caminho.parent.is_dir():
        raise FileNotFoundError(f"Diretório do perfil não existe: {caminho.parent}")
    fd, temporario = tempfile.mkstemp(prefix=f".{caminho.name}.", suffix=".tmp", dir=caminho.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as arquivo:
            json.dump(perfil, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    except BaseException:
        Path(temporario).unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="comando", required=True)
    rebuild = sub.add_parser("rebuild")
    rebuild.add_argument("--log", type=Path, required=True)
    rebuild.add_argument("--perfil", type=Path, required=True)
    rebuild.add_argument("--config", type=Path)
    rebuild.add_argument("--confirmar-gravacao-local", action="store_true", required=True)
    export = sub.add_parser("export")
    export.add_argument("--log", type=Path, required=True)
    export.add_argument("--perfil", type=Path, required=True)
    export.add_argument("--saida", type=Path, required=True)
    export.add_argument("--confirmar-gravacao-local", action="store_true", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("--perfil", type=Path, required=True)
    delete = sub.add_parser("delete")
    delete.add_argument("--perfil", type=Path, required=True)
    delete.add_argument("--confirmar-exclusao-local", action="store_true", required=True)
    args = parser.parse_args(argv)
    if args.comando == "inspect":
        print(args.perfil.read_text(encoding="utf-8"), end="")
        return 0
    if args.comando == "delete":
        args.perfil.unlink(missing_ok=True)
        print(json.dumps({"status": "removido", "perfil": str(args.perfil)}, ensure_ascii=False))
        return 0
    eventos = ler_eventos(args.log)
    if args.comando == "rebuild":
        configuracao = json.loads(args.config.read_text(encoding="utf-8")) if args.config else None
        salvar_perfil_atomico(args.perfil, reconstruir_perfil(eventos, configuracao))
        return 0
    pacote = {"events": eventos, "profile": json.loads(args.perfil.read_text(encoding="utf-8"))}
    if not args.saida.parent.is_dir():
        raise FileNotFoundError(f"Diretório de saída não existe: {args.saida.parent}")
    args.saida.write_text(json.dumps(pacote, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
