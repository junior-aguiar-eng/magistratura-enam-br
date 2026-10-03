"""Gera perfil descritivo por leitura de metadados/classificações declarados.

Não coleta documentos, confirma hashes de PDFs, mede acertos ou aprova mérito.
Um registro synthetic nunca se torna referência empírica por ter contagens.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

FORMATS = ("direto", "numerado", "vf", "associacao")
PROFILE_KIND = "exam_calibration_profile"
SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "modelos/pedagogia/exam-corpus.schema.json"
)


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _official_url(value: str) -> bool:
    parsed = urlsplit(value)
    host = parsed.hostname or ""
    return (
        parsed.scheme == "https"
        and parsed.username is None
        and parsed.password is None
        and parsed.port in (None, 443)
        and (host.endswith((".jus.br", ".gov.br")) or host == "conhecimento.fgv.br")
    )


def validate_corpus(corpus: dict) -> None:
    """Valida contrato e referências declaradas, sem consulta ou aprovação humana."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    if not isinstance(corpus, dict) or next(validator.iter_errors(corpus), None):
        raise ValueError("Registro de corpus incompatível com schema")
    if not _official_url(corpus["official_source"]["url"]):
        raise ValueError("Origem exige HTTPS de órgão público ou banca admitida")
    key = corpus["answer_key"]
    if "url" in key and not _official_url(key["url"]):
        raise ValueError("Gabarito não tem origem oficial admitida")
    questions = corpus["questions"]
    if len(questions) > corpus["expected_questions"]:
        raise ValueError("Mais itens cadastrados que o total declarado")
    identifiers = [question["id"] for question in questions]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("ID de questão repetido")
    for question in questions:
        review_ids = [review["id"] for review in question["reviews"]]
        if len(set(review_ids)) != len(review_ids):
            raise ValueError("ID de revisão repetido no item")
        if "resolution" in question:
            resolution = question["resolution"]
            if resolution["selected_review_id"] not in review_ids:
                raise ValueError("Resolução aponta revisão ausente")
            if any(
                resolution["date"] < review["date"] for review in question["reviews"]
            ):
                raise ValueError(
                    "Resolução anterior à revisão não resolve a divergência"
                )


def _classification(question: dict) -> tuple[dict | None, list[str]]:
    reviews = question["reviews"]
    if not reviews:
        return None, ["review_missing"]
    if "resolution" in question:
        selected = next(
            review
            for review in reviews
            if review["id"] == question["resolution"]["selected_review_id"]
        )
    else:
        signatures = set()
        for review in reviews:
            difficulty = review.get("difficulty")
            signatures.add(
                _canonical(
                    [
                        review["format"],
                        review["discipline"],
                        review["point_source"],
                        [difficulty["label"], difficulty["method"]]
                        if difficulty
                        else None,
                    ]
                )
            )
        if len(signatures) != 1:
            return None, ["classification_unresolved"]
        selected = reviews[0]
    if any(
        selected[field] is None for field in ("format", "discipline", "point_source")
    ):
        return None, ["classification_incomplete"]
    return selected, []


def _distribution(counts: dict, denominator: int) -> dict:
    return {
        "sample_size": sum(counts.values()),
        "denominator": denominator,
        "counts": counts,
    }


def build_calibration_profile(corpus: dict) -> dict:
    """Distribuições somente dos itens elegíveis; exclusões e cobertura explícitas."""
    validate_corpus(corpus)
    formats = dict.fromkeys(FORMATS, 0)
    disciplines, point_sources, difficulties = Counter(), Counter(), Counter()
    estimates, exclusions = [], []
    reviewed = eligible = 0
    for question in corpus["questions"]:
        selected, reasons = _classification(question)
        reviewed += selected is not None
        if question["status"] != "valida":
            reasons.append(
                "question_annulled"
                if question["status"] == "anulada"
                else "question_pending"
            )
        if corpus["answer_key"]["status"] != "definitivo":
            reasons.append("answer_key_not_final")
        if reasons:
            exclusions.append({"question_id": question["id"], "reasons": reasons})
            continue
        eligible += 1
        formats[selected["format"]] += 1
        disciplines[selected["discipline"]] += 1
        point_sources[selected["point_source"]["type"]] += 1
        difficulty = selected.get("difficulty")
        if difficulty:
            difficulties[difficulty["label"]] += 1
            estimates.append({"question_id": question["id"], **difficulty})
    registered = len(corpus["questions"])
    expected = corpus["expected_questions"]
    warnings = []
    if eligible < 8:
        warnings.append("small_sample_no_generalization")
    if corpus["evidence_kind"] == "synthetic":
        warnings.append("synthetic_not_empirical")
    return {
        "schema_version": "1.0.0",
        "kind": PROFILE_KIND,
        "status": "sem_calibracao"
        if not eligible
        else "parcial"
        if eligible < expected
        else "descritivo",
        "empirical_reference_available": corpus["evidence_kind"] == "official"
        and eligible > 0,
        "verification_basis": "declared_document_review",
        "corpus_sha256": hashlib.sha256(_canonical(corpus).encode("utf-8")).hexdigest(),
        "origin": {
            field: copy.deepcopy(corpus[field])
            for field in (
                "corpus_id",
                "evidence_kind",
                "edition",
                "exam_type",
                "date",
                "official_source",
                "document_review",
                "answer_key",
            )
        },
        "coverage": {
            "expected": expected,
            "registered": registered,
            "reviewed": reviewed,
            "eligible": eligible,
            "excluded": registered - eligible,
            "missing": expected - registered,
        },
        "distributions": {
            "formats": _distribution(formats, eligible),
            "disciplines": _distribution(dict(disciplines), eligible),
            "point_sources": _distribution(dict(point_sources), eligible),
            "difficulty": _distribution(dict(difficulties), len(estimates)),
        },
        "difficulty_estimates": estimates,
        "exclusions": exclusions,
        "warnings": warnings,
        "not_checked": [
            "document_bytes_not_verified",
            "juridical_merit",
            "representativeness",
            "difficulty_not_official",
            "accuracy_not_measured",
        ],
        "corpus": copy.deepcopy(corpus),
    }


def validate_calibration_profile(profile: dict) -> None:
    """Recalcula perfil inteiro da evidência incluída; hash não prova autenticidade."""
    if (
        not isinstance(profile, dict)
        or profile.get("kind") != PROFILE_KIND
        or not isinstance(profile.get("corpus"), dict)
    ):
        raise ValueError("Perfil de calibração não reconhecido")
    if _canonical(profile) != _canonical(build_calibration_profile(profile["corpus"])):
        raise ValueError("Perfil diverge do registro de corpus")


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Chave JSON repetida")
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    raise ValueError("Número JSON não finito")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        corpus = json.loads(
            args.corpus.read_text(encoding="utf-8-sig"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        result = build_calibration_profile(corpus)
    except ValueError, OSError, UnicodeError:
        result = {
            "status": "entrada_invalida",
            "errors": [
                {
                    "code": "invalid_corpus",
                    "message": "Registro ilegível ou inválido; conteúdo não reproduzido.",
                }
            ],
        }
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if "errors" in result else 0


if __name__ == "__main__":
    raise SystemExit(main())
