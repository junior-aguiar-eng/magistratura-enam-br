import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


def carregar_json(caminho):
    return json.loads(caminho.read_text(encoding="utf-8"))


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def rota(**alteracoes):
    base = {
        "schema_version": "1.0.0",
        "skill_ativa": "estudar-direito-magistratura",
        "modalidade_ativa": "questao_objetiva",
        "tema_ativo": "controle de constitucionalidade",
        "etapa": "aguardando_resposta",
        "pendencia": {
            "tipo": "questao_objetiva",
            "descricao": "Questão 1 aguarda alternativa.",
            "aguarda_resposta": True,
        },
        "rota_suspensa": None,
        "politica_fontes": "acervo_com_validacao_oficial",
    }
    base.update(alteracoes)
    return base


def estado(**alteracoes):
    base = {
        "skill": "estudar-direito-magistratura",
        "modalidade": "questao_objetiva",
        "tema": "controle de constitucionalidade",
        "etapa": "aguardando_resposta",
        "tem_pendencia": True,
        "tem_rota_suspensa": False,
    }
    base.update(alteracoes)
    return base


def transicao(kind, origem=None, destino=None, **alteracoes):
    base = {
        "schema_version": "1.0.0",
        "from": origem or estado(),
        "to": destino or estado(),
        "kind": kind,
        "reason": "Pedido atual do candidato.",
        "requires_confirmation": False,
        "preserves": ["politica_fontes"],
    }
    base.update(alteracoes)
    return base


def test_rotas_validas_respeitam_skill_modalidade():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "session-route.schema.json")
    validator = Draft202012Validator(schema)

    fixtures = [
        rota(),
        rota(skill_ativa="acompanhar-percurso-magistratura", modalidade_ativa="roteamento", etapa="ambientacao", pendencia=None),
        rota(skill_ativa="curar-informativos-stf-stj", modalidade_ativa="curadoria_informativo", etapa="em_execucao", pendencia=None),
        rota(skill_ativa="comparar-materiais-enam", modalidade_ativa="comparacao_material", etapa="em_execucao", pendencia=None),
        rota(skill_ativa="planejar-jurisprudencia", modalidade_ativa="revisao_julgado", etapa="em_execucao", pendencia=None),
    ]

    assert all(validator.is_valid(item) for item in fixtures)


@pytest.mark.parametrize(
    "fixture",
    [
        rota(skill_ativa="skill-inexistente"),
        rota(skill_ativa="planejar-jurisprudencia", modalidade_ativa="questao_objetiva"),
        {**rota(), "persistir": True},
    ],
)
def test_rotas_invalidas_sao_rejeitadas(fixture):
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "session-route.schema.json")
    assert not Draft202012Validator(schema).is_valid(fixture)


def test_transicoes_cobrem_fluxo_completo():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "transition.schema.json")
    validator = Draft202012Validator(schema)
    suspensa = estado(etapa="suspensa", tem_rota_suspensa=True)
    ativa = estado(etapa="em_execucao", tem_pendencia=False)
    fixtures = [
        transicao("continuidade"),
        transicao("mudanca_tema", destino=estado(tema="prescrição e decadência")),
        transicao("mudanca_modalidade", destino=estado(modalidade="explicacao", tem_pendencia=False)),
        transicao("mudanca_skill", destino=estado(skill="curar-informativos-stf-stj", modalidade="curadoria_informativo", tem_pendencia=False)),
        transicao("suspensao", destino=suspensa, preserves=["pendencia", "politica_fontes"]),
        transicao("retomada", origem=suspensa, destino=ativa),
        transicao("encerramento", destino=estado(etapa="encerrada", tem_pendencia=False)),
    ]

    assert all(validator.is_valid(item) for item in fixtures)


def test_retomada_sem_rota_suspensa_e_persistencia_implicita_sao_rejeitadas():
    schema = carregar_json(PLUGIN_ROOT / "modelos" / "pedagogia" / "transition.schema.json")
    validator = Draft202012Validator(schema)
    sem_rota = transicao("retomada")
    persistencia = deepcopy(transicao("continuidade"))
    persistencia["persistir"] = True

    assert not validator.is_valid(sem_rota)
    assert not validator.is_valid(persistencia)
