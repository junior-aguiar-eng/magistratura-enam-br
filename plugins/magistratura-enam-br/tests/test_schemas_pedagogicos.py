import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "modelos" / "pedagogia"


def carregar_schema(nome: str) -> dict:
    schema = json.loads((SCHEMAS / nome).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


@pytest.fixture
def evento_valido() -> dict:
    return {
        "schema_version": "1.0.0",
        "event_id": "evt_01a06d61-62eb-71f1-b7c0-5e19a67c47dc",
        "occurred_at": "2026-09-04T12:00:00Z",
        "skill": "estudar-direito-magistratura",
        "content_ref": {
            "content_id": "cc-prescricao-decadencia",
            "source_type": "material_candidato",
            "locator": "capitulo-3",
        },
        "activity": {"modality": "questao_objetiva", "attempt_observed": True},
        "performance": {
            "result": "parcial",
            "error_types": ["distincao"],
            "domain_evidence": ["evocacao_regra"],
            "confidence": "baixa",
        },
        "routing": {
            "target_skill": "estudar-direito-magistratura",
            "reason_codes": ["remediacao_aberta"],
        },
    }


def test_learning_event_aceita_fixture_valida(evento_valido):
    Draft202012Validator(carregar_schema("learning-event.schema.json")).validate(evento_valido)


def criar_evento_v2() -> dict:
    return {
        "schema_version": "2.0.0",
        "event_id": "evt_21a06d61-62eb-71f1-b7c0-5e19a67c47dc",
        "occurred_at": "2026-09-05T12:00:00Z",
        "skill": "estudar-direito-magistratura",
        "content_ref": {
            "kind": "questao",
            "id": "civil-prescricao-001",
            "disciplina": "Direito Civil",
            "tema": "Prescrição e decadência",
            "subtema": "Termo inicial",
            "source_refs": ["CC-art-189"],
            "source_state": "verificada",
            "source_version": "2026-09-05",
        },
        "activity": {
            "activity_id": "atividade-civil-prescricao-001",
            "modality": "questao_objetiva",
            "attempt_observed": True,
            "assistance_level": "nenhuma",
        },
        "performance": {
            "result": "correto",
            "error_types": [],
            "domain_evidence": ["aplicacao_fatos_novos"],
            "confidence": None,
        },
        "routing": {"target_skill": None, "reason_codes": []},
    }


def test_learning_event_v2_exige_identidade_versao_e_assistencia():
    schema = carregar_schema("learning-event.schema.json")
    evento = criar_evento_v2()
    Draft202012Validator(schema).validate(evento)
    for container, field in (
        ("content_ref", "source_version"),
        ("activity", "activity_id"),
        ("activity", "assistance_level"),
    ):
        invalido = json.loads(json.dumps(evento))
        del invalido[container][field]
        with pytest.raises(ValidationError):
            Draft202012Validator(schema).validate(invalido)


def test_profile_settings_rejeita_dado_pessoal():
    schema = carregar_schema("profile-settings.schema.json")
    configuracao = {"schema_version": "1.0.0", "objectives": [], "preferences": {}}
    Draft202012Validator(schema).validate(configuracao)
    configuracao["email"] = "candidato@example.com"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(configuracao)


@pytest.mark.parametrize(
    ("caminho", "valor"),
    [
        (("activity", "modality"), "aula_livre"),
        (("performance", "result"), "quase_correto"),
        (("performance", "error_types"), ["desatencao"]),
        (("performance", "domain_evidence"), ["nota_global"]),
    ],
)
def test_learning_event_rejeita_categoria_divergente(evento_valido, caminho, valor):
    evento_valido[caminho[0]][caminho[1]] = valor

    with pytest.raises(ValidationError):
        Draft202012Validator(carregar_schema("learning-event.schema.json")).validate(evento_valido)


def test_learning_event_rejeita_erro_sem_tentativa_observada(evento_valido):
    evento_valido["activity"]["attempt_observed"] = False

    with pytest.raises(ValidationError):
        Draft202012Validator(carregar_schema("learning-event.schema.json")).validate(evento_valido)


def test_comparador_nao_pode_registrar_dominio_ou_erro(evento_valido):
    evento_valido["skill"] = "comparar-materiais-enam"

    with pytest.raises(ValidationError):
        Draft202012Validator(carregar_schema("learning-event.schema.json")).validate(evento_valido)


def test_candidate_profile_aceita_fixture_minima_e_rejeita_email():
    schema = carregar_schema("candidate-profile.schema.json")
    perfil = {
        "schema_version": "1.0.0",
        "updated_at": "2026-09-04T12:00:00Z",
        "objectives": ["Magistratura estadual"],
        "preferences": {"feedback_mode": "completo"},
        "competencies": [],
        "open_remediations": [],
    }
    Draft202012Validator(schema).validate(perfil)
    perfil["email"] = "candidato@example.com"

    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(perfil)


def test_review_recommendation_aceita_fixture_valida():
    schema = carregar_schema("review-recommendation.schema.json")
    recomendacao = {
        "schema_version": "1.0.0",
        "policy": "fixed_v1",
        "base_interval_days": 7,
        "suggested_interval_days": 7,
        "reason_codes": ["fixed_policy_preserved"],
        "shadow_mode": True,
    }

    Draft202012Validator(schema).validate(recomendacao)
