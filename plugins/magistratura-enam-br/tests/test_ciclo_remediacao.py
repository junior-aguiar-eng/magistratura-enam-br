import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _planner():
    path = ROOT / "skills" / "planejar-jurisprudencia" / "scripts" / "atualizar_esteira.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("atualizar_esteira", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _evento(*, result="correto", content_id="STJ-REsp-123", remediation_id="rem-1"):
    return {
        "schema_version": "1.1.0",
        "event_id": "evt_1234567890abcdefghij",
        "occurred_at": "2026-09-04T12:00:00Z",
        "skill": "estudar-direito-magistratura",
        "remediation_id": remediation_id,
        "content_ref": {
            "kind": "precedente",
            "id": content_id,
            "disciplina": "Direito Civil",
            "tema": "Responsabilidade civil",
            "subtema": "Dano moral",
            "source_refs": ["https://processo.stj.jus.br/123"],
            "source_state": "confirmado",
        },
        "activity": {"modality": "questao_objetiva", "attempt_observed": True},
        "performance": {
            "result": result,
            "error_types": [],
            "domain_evidence": ["aplicacao_fatos_novos"],
            "confidence": "alta",
        },
        "routing": {
            "target_skill": "planejar-jurisprudencia",
            "reason_codes": ["remediacao_concluida"],
        },
    }


def test_ciclo_fecha_somente_com_evento_correto_confirmado_do_mesmo_conteudo():
    planner = _planner()
    remediacoes = [
        {
            "remediation_id": "rem-1",
            "content_ref_id": "STJ-REsp-123",
            "resultado_revisao": "erro",
            "encaminhamento": "questao_objetiva",
            "Feito?": "",
        }
    ]

    assert not planner.concluir_remediacao_por_evento(remediacoes, _evento(), confirmado=False)
    assert not planner.concluir_remediacao_por_evento(
        remediacoes, _evento(content_id="outro"), confirmado=True
    )
    assert not planner.concluir_remediacao_por_evento(
        remediacoes, _evento(result="parcial"), confirmado=True
    )
    evento_invalido = _evento()
    evento_invalido["schema_version"] = "1.0.0"
    assert not planner.concluir_remediacao_por_evento(
        remediacoes, evento_invalido, confirmado=True
    )
    assert planner.concluir_remediacao_por_evento(remediacoes, _evento(), confirmado=True)
    assert remediacoes[0]["Feito?"] == "sim"
    assert remediacoes[0]["resultado_remediacao"] == "remediacao_concluida"
