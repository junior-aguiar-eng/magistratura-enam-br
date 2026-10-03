"""Audita estrutura e padrões editoriais, por leitura, sem certificar mérito jurídico.

Relatórios com gabarito são privados: distribuições podem revelar uma chave em
amostras pequenas. Não use a saída como apresentação pré-tentativa ao candidato.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

FORMATS = ("direto", "numerado", "vf", "associacao")
OPTIONS = tuple("ABCDE")
ABSOLUTES = (
    "sempre",
    "nunca",
    "apenas",
    "somente",
    "exclusivamente",
    "necessariamente",
    "em qualquer caso",
    "em nenhuma hipotese",
)
MIN_PATTERN_SAMPLE = 8
PATTERN_THRESHOLD = 0.75


def _normal(text: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", text.casefold())
        if not unicodedata.combining(char)
    )


def _plain(line: str) -> str:
    line = re.sub(r"^\s*>\s?", "", line).strip()
    line = line.replace("**", "").replace("__", "").replace("`", "")
    line = re.sub(r"(?<!\w)[*_]([^*_]+)[*_](?!\w)", r"\1", line)
    return line


def _infer_format(
    prompt: str, alternatives: list[tuple[str, str]]
) -> Literal["direto", "numerado", "vf", "associacao"]:
    text = _normal(prompt)
    if "coluna" in text and (
        "assoc" in text or "coluna ii" in text or "segunda coluna" in text
    ):
        return "associacao"
    if len(alternatives) == 5 and all(
        re.fullmatch(r"(?:[VF](?:\s*[-–—,;/]\s*[VF])+|[VF]{2,})[.!]?", option.strip())
        for _, option in alternatives
    ):
        return "vf"
    if re.search(r"\bv\s*[/–—-]\s*f\b|verdadeir[oa].*fals[oa]|assinale\s+v\b", text):
        return "vf"
    if (
        len(re.findall(r"(?m)^\s*(?:I|II|III|IV|[1-9]\d{0,2})[.)]\s", prompt)) >= 2
        or "afirmativas" in text
    ):
        return "numerado"
    return "direto"


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Chave JSON repetida; entrada ambígua")
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    raise ValueError("Número JSON não finito")


def _load_json(text: str) -> object:
    return json.loads(
        text, object_pairs_hook=_unique_object, parse_constant=_reject_constant
    )


@dataclass
class AuditQuestion:
    id: str
    format: Literal["direto", "numerado", "vf", "associacao"]
    prompt: str
    alternatives: list[tuple[str, str]]
    correct_option: str | None = field(default=None, repr=False)


def parse_question_block(
    text: str, *, format: Literal["markdown", "json"]
) -> list[AuditQuestion]:
    """Markdown com cabeçalhos Questão ID; JSON com projeções de sessão.

    Uma questão sem cabeçalho recebe ID "1". Marcadores de alternativas são
    linhas A) ou A. (também com bullet/ênfase); indentação >=4 é continuação.
    Duplicatas são preservadas para a auditoria, nunca convertidas em dict.
    """
    if format == "json":
        payload = _load_json(text)
        if not isinstance(payload, list):
            raise ValueError("Bloco JSON deve ser array de questões")
        result = []
        for item in payload:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("session_id"), str)
                or not isinstance(item.get("prompt"), str)
                or not isinstance(item.get("alternatives"), list)
            ):
                raise ValueError("Projeção de questão não interpretável")  # noqa: TRY004 - valor inválido no documento JSON
            alternatives = []
            for option in item["alternatives"]:
                if (
                    not isinstance(option, dict)
                    or not isinstance(option.get("id"), str)
                    or not isinstance(option.get("text"), str)
                ):
                    raise ValueError("Alternativa JSON não interpretável")  # noqa: TRY004 - valor inválido no documento JSON
                alternatives.append((option["id"], option["text"]))
            question_format = item.get(
                "format", _infer_format(item["prompt"], alternatives)
            )
            if not isinstance(question_format, str) or (
                "correct_option" in item and not isinstance(item["correct_option"], str)
            ):
                raise ValueError("Formato ou chave JSON não interpretável")
            result.append(
                AuditQuestion(
                    item["session_id"],
                    question_format,
                    item["prompt"],
                    alternatives,
                    item.get("correct_option"),
                )
            )
        return result
    if format != "markdown":
        raise ValueError("Transporte não suportado")
    if not text.strip():
        return []
    lines = text.splitlines()
    if (
        lines[0].strip() in ("```", "```markdown", "```md")
        and lines[-1].strip() == "```"
    ):
        lines = lines[1:-1]
    if any(line.strip().startswith("```") for line in lines):
        raise ValueError("Bloco cercado não interpretável")
    sections: list[tuple[str, list[str]]] = []
    current: list[str] = []
    identifier = "1"
    had_heading = False
    for line in lines:
        heading = re.match(
            r"(?i)^quest(?:ão|ao)\s+([\w.:-]+)(?:\s|$)",
            re.sub(r"^#{1,6}\s+", "", _plain(line)),
        )
        if heading and len(line) - len(line.lstrip()) < 4:
            if _leaks(line):
                raise ValueError("Marcador explícito de solução no cabeçalho")
            if had_heading:
                sections.append((identifier, current))
            elif current:
                raise ValueError("Texto anterior ao primeiro cabeçalho")
            identifier, current = heading.group(1).rstrip(":"), []
            had_heading = True
        elif line.strip():
            current.append(line)
    if current or had_heading:
        sections.append((identifier, current))
    result = []
    for identifier, section in sections:
        prompt_lines: list[str] = []
        alternatives: list[tuple[str, str]] = []
        for line in section:
            cleaned = _plain(line)
            if alternatives and (
                re.match(r"^#{1,6}\s+", cleaned)
                or _normal(cleaned).rstrip(":").strip()
                in (
                    "correcao",
                    "justificativa",
                    "gabarito",
                    "resposta comentada",
                    "resolucao",
                    "solucao",
                )
            ):
                raise ValueError(
                    "Seção posterior às alternativas não integra uma questão"
                )
            marker = re.match(r"^(?:[-+*]\s+)?([A-Z])[.)]\s*(.*)$", cleaned)
            # I/V/X em assertivas não são opções antes do primeiro marcador A–E.
            if (
                marker
                and (alternatives or marker.group(1) in OPTIONS)
                and len(line) - len(line.lstrip()) < 4
            ):
                alternatives.append((marker.group(1), marker.group(2)))
            elif alternatives:
                label, previous = alternatives[-1]
                alternatives[-1] = (label, previous + "\n" + cleaned)
            else:
                prompt_lines.append(cleaned)
        if not alternatives or not prompt_lines:
            raise ValueError("Questão Markdown não interpretável")
        prompt = "\n".join(prompt_lines)
        result.append(
            AuditQuestion(
                identifier, _infer_format(prompt, alternatives), prompt, alternatives
            )
        )
    return result


def _issue(code: str, message: str, identifier: str | None = None) -> dict:
    result = {"code": code, "message": message}
    if identifier is not None:
        result["question_id"] = identifier
    return result


def _leaks(text: str) -> bool:
    # Preserve letter case: lowercase a/e may be an article or conjunction.
    text = "".join(
        char
        for char in unicodedata.normalize("NFKD", _plain(text))
        if not unicodedata.combining(char)
    )
    for marker in re.finditer(
        r"\b(?:gabarito|resposta(?: correta)?|alternativa correta|solucao)\s*(?::|=|e\s+)\s*"
        r"(?:(?:letra|alternativa)\s+(?P<label>[a-e])\b|(?P<bare>[a-e])\b"
        r"(?:[ \t]+(?P<following>\w+))?)",
        text,
        re.IGNORECASE,
    ):
        letter = marker.group("bare")
        following = (marker.group("following") or "").casefold()
        if (
            marker.group("label")
            or letter.isupper()
            or letter.casefold() not in {"a", "e"}
            or not following
            or following in {"porque", "pois", "porquanto"}
        ):
            return True
    return bool(re.search(r"[✓✔✅]|\((?:correta|gabarito)\)", text, re.IGNORECASE))


def _absolute_counts(text: str) -> dict[str, int]:
    normalized = _normal(text)
    return {
        term: len(re.findall(r"\b" + re.escape(term) + r"\b", normalized))
        for term in ABSOLUTES
    }


def _pattern(matches: int, denominator: int) -> dict:
    return {
        "sample_size": matches,
        "denominator": denominator,
        "fraction": matches / denominator if denominator else None,
    }


def audit_question_block(
    questions: list[AuditQuestion],
    answers: dict[str, str] | None = None,
    profile: dict | None = None,
) -> dict:
    """Nunca devolve conteúdo ou gabarito individual; status é só estrutural.

    Padrões agregados usam somente questões com estrutura e chave compatíveis.
    Formatos e tamanhos também são medidos sem chave, com cobertura explícita.
    """
    errors, warnings, not_checked = (
        [],
        [],
        [
            _issue(
                "juridical_merit",
                "Fundamentação, fontes, plausibilidade e unicidade jurídica exigem revisão humana.",
            ),
            _issue(
                "format_calibration",
                "Representatividade do corpus e fidelidade ao ENAM não certificadas; não impor quota automática de formatos.",
            ),
        ],
    )
    if profile is not None and not isinstance(profile, dict):
        errors.append(_issue("invalid_profile", "Perfil deve ser objeto JSON."))
    calibration_profile = None
    if isinstance(profile, dict) and profile.get("kind") == "exam_calibration_profile":
        from calibrar_provas import validate_calibration_profile

        try:
            validate_calibration_profile(profile)
            if profile["empirical_reference_available"]:
                calibration_profile = profile
            else:
                not_checked.append(
                    _issue(
                        "profile_not_empirical",
                        "Perfil sintético ou sem itens elegíveis; não serve como referência empírica.",
                    )
                )
        except ValueError:
            errors.append(
                _issue(
                    "invalid_profile",
                    "Perfil diverge do corpus ou contém registro inválido.",
                )
            )
    elif profile is not None:
        not_checked.append(
            _issue(
                "profile_not_validated",
                "Perfil não reconhecido pelo contrato do corpus; não ativa comparação ou quotas.",
            )
        )
    if answers is not None and not isinstance(answers, dict):
        errors.append(
            _issue("invalid_answers", "Gabarito deve mapear IDs para letras A–E.")
        )
        answers = {}
    if not questions:
        errors.append(_issue("empty_block", "Nenhuma questão interpretável no bloco."))
    ids = Counter(q.id for q in questions if isinstance(q.id, str))
    if answers:
        for identifier in answers:
            if identifier not in ids:
                errors.append(
                    _issue("unknown_answer_id", "Gabarito contém ID ausente do bloco.")
                )
    key_counts = dict.fromkeys(OPTIONS, 0)
    format_counts = dict.fromkeys(FORMATS, 0)
    length_items: list[dict] = []
    absolute_counts = dict.fromkeys(ABSOLUTES, 0)
    alternative_count = with_text = with_absolute = formats_recognized = 0
    covered = length_matches = absolute_matches = longest_run = run = 0
    previous_answer = None
    for index, question in enumerate(questions, 1):
        identifier = (
            question.id
            if isinstance(question.id, str) and re.fullmatch(r"[\w.:-]+", question.id)
            else f"item:{index}"
        )
        start = len(errors)
        if identifier != question.id:
            errors.append(
                _issue("invalid_id", "ID vazio ou não interpretável.", identifier)
            )
        if ids.get(question.id, 0) > 1:
            errors.append(_issue("duplicate_id", "ID de questão repetido.", identifier))
        if question.format not in FORMATS:
            errors.append(
                _issue(
                    "unsupported_question_format",
                    "Formato de questão não suportado.",
                    identifier,
                )
            )
        else:
            format_counts[question.format] += 1
            formats_recognized += 1
        if not isinstance(question.prompt, str) or not question.prompt.strip():
            errors.append(_issue("empty_prompt", "Enunciado ausente.", identifier))
        elif _leaks(question.prompt):
            errors.append(
                _issue(
                    "answer_leak", "Marcador explícito de solução no texto.", identifier
                )
            )
        options = (
            question.alternatives if isinstance(question.alternatives, list) else []
        )
        alternative_count += len(options)
        labels, sizes, counts = [], {}, {}
        for option in options:
            if (
                not isinstance(option, (tuple, list))
                or len(option) != 2
                or not isinstance(option[0], str)
                or not isinstance(option[1], str)
            ):
                errors.append(
                    _issue(
                        "invalid_alternative",
                        "Alternativa não interpretável.",
                        identifier,
                    )
                )
                continue
            label, text = option
            labels.append(label)
            if not text.strip():
                errors.append(
                    _issue("empty_alternative", "Alternativa sem texto.", identifier)
                )
            if _leaks(text):
                errors.append(
                    _issue(
                        "answer_leak",
                        "Marcador explícito de solução no texto.",
                        identifier,
                    )
                )
            item_counts = _absolute_counts(text)
            sizes[label], counts[label] = len(text), sum(item_counts.values())
            length_items.append(
                {
                    "question_id": identifier,
                    "option": label,
                    "characters": len(text),
                    "words": len(re.findall(r"\b\w+\b", text)),
                }
            )
            with_text += 1
            with_absolute += bool(counts[label])
            for term, count in item_counts.items():
                absolute_counts[term] += count
        if len(labels) != 5 or Counter(labels) != Counter(OPTIONS):
            errors.append(
                _issue(
                    "alternative_labels",
                    "Exigir exatamente A, B, C, D e E, sem repetição ou opção extra.",
                    identifier,
                )
            )
        internal = question.correct_option
        external_present = answers is not None and question.id in answers
        external = answers.get(question.id) if external_present else None
        if internal is not None and (
            not isinstance(internal, str) or internal not in OPTIONS
        ):
            errors.append(
                _issue("invalid_answer", "Chave interna fora de A–E.", identifier)
            )
        if external_present and (
            not isinstance(external, str) or external not in OPTIONS
        ):
            errors.append(
                _issue("invalid_answer", "Chave externa fora de A–E.", identifier)
            )
        if internal is not None and external_present and internal != external:
            errors.append(
                _issue(
                    "contradictory_answer",
                    "Chaves interna e externa divergem.",
                    identifier,
                )
            )
        key = external if external_present else internal
        if len(errors) == start and key in OPTIONS:
            covered += 1
            key_counts[key] += 1
            length_matches += sizes[key] > max(
                sizes[other] for other in OPTIONS if other != key
            )
            absolute_matches += counts[key] == 0 and all(
                counts[other] > 0 for other in OPTIONS if other != key
            )
            run = run + 1 if key == previous_answer else 1
            longest_run = max(longest_run, run)
            previous_answer = key
        else:
            run, previous_answer = 0, None
    if covered < len(questions):
        not_checked.append(
            _issue(
                "answer_coverage",
                "Checagens com chave omitidas para itens sem gabarito válido ou estrutura elegível; resultado não é aprovação global.",
            )
        )
    if longest_run >= 3:
        warnings.append(
            _issue(
                "repeated_key_run",
                "Ao menos três chaves consecutivas iguais; aviso editorial, não reprovação jurídica.",
            )
        )
    for code, matches in (
        ("length_pattern", length_matches),
        ("absolute_pattern", absolute_matches),
    ):
        if covered >= MIN_PATTERN_SAMPLE and matches / covered > PATTERN_THRESHOLD:
            warnings.append(
                _issue(
                    code,
                    "Padrão em mais de 75% de pelo menos oito itens elegíveis; heurística do projeto, não estatística oficial ou defeito jurídico comprovado.",
                )
            )
    calibration = {"performed": False}
    if calibration_profile is not None and not errors and formats_recognized:
        reference = calibration_profile["distributions"]["formats"]
        denominator = reference["denominator"]
        calibration = {
            "performed": True,
            "reference_corpus_sha256": calibration_profile["corpus_sha256"],
            "reference_sample_size": denominator,
            "block_sample_size": formats_recognized,
            "format_deltas": {
                name: format_counts[name] / formats_recognized
                - reference["counts"][name] / denominator
                for name in FORMATS
            },
        }
        if denominator < 8 or formats_recognized < 8:
            warnings.append(
                _issue(
                    "calibration_small_sample",
                    "Comparação descritiva com amostra menor que oito; não generaliza padrão nem impõe quota.",
                )
            )
        not_checked.append(
            _issue(
                "calibration_scope",
                "Comparação limitada a formatos do subconjunto revisado da edição declarada; bytes oficiais, representatividade e dificuldade não certificados.",
            )
        )
    return {
        "schema_version": "1.0.0",
        "questions_count": len(questions),
        "status": "reprovado_estruturalmente"
        if errors
        else "checagem_parcial"
        if covered < len(questions)
        else "aprovado_estruturalmente",
        "errors": errors,
        "warnings": warnings,
        "not_checked": not_checked,
        "metrics": {
            "answer_coverage": {"sample_size": covered, "denominator": len(questions)},
            "answer_distribution": {
                "sample_size": covered,
                "denominator": covered,
                "counts": key_counts,
            },
            "format_distribution": {
                "sample_size": formats_recognized,
                "denominator": formats_recognized,
                "counts": format_counts,
            },
            "alternative_lengths": {
                "sample_size": with_text,
                "denominator": alternative_count,
                "items": length_items,
            },
            "absolute_frequency": {
                "sample_size": with_absolute,
                "denominator": with_text,
                "counts": absolute_counts,
            },
            "length_pattern": _pattern(length_matches, covered),
            "absolute_pattern": _pattern(absolute_matches, covered),
            "key_runs": {
                "sample_size": covered,
                "denominator": covered,
                "longest_run": longest_run,
            },
            "profile_provided": profile is not None,
            "calibration": calibration,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questoes", type=Path, required=True)
    parser.add_argument("--formato", choices=("markdown", "json"), required=True)
    parser.add_argument("--gabarito", type=Path)
    parser.add_argument("--perfil", type=Path)
    args = parser.parse_args(argv)
    try:
        questions = parse_question_block(
            args.questoes.read_text(encoding="utf-8-sig"), format=args.formato
        )
        answers = (
            _load_json(args.gabarito.read_text(encoding="utf-8-sig"))
            if args.gabarito
            else None
        )
        profile = (
            _load_json(args.perfil.read_text(encoding="utf-8-sig"))
            if args.perfil
            else None
        )
        if (args.gabarito and not isinstance(answers, dict)) or (
            args.perfil and not isinstance(profile, dict)
        ):
            raise ValueError("Gabarito/perfil deve ser objeto JSON")
        result = audit_question_block(questions, answers, profile)
    except ValueError, OSError, UnicodeError:
        result = audit_question_block([])
        result["errors"] = [
            _issue(
                "input_error",
                "Entrada ilegível, inválida ou não interpretável; conteúdo não reproduzido.",
            )
        ]
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
