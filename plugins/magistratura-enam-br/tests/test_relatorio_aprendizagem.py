import importlib.util
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "relatorio_aprendizagem.py"


def _module():
    spec = importlib.util.spec_from_file_location("relatorio_aprendizagem", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _evento(
    dia,
    modalidade,
    resultado,
    *,
    tentativa=True,
    erros=(),
    evidencias=(),
    confianca=None,
):
    return {
        "occurred_at": f"2026-09-{dia:02d}T12:00:00Z",
        "activity": {
            "modality": modalidade,
            "attempt_observed": tentativa,
        },
        "performance": {
            "result": resultado,
            "error_types": list(erros),
            "domain_evidence": list(evidencias),
            "confidence": confianca,
        },
    }


def test_relatorio_calcula_metricas_sem_pontuacao_global():
    modulo = _module()
    eventos = [
        _evento(1, "questao_objetiva", "correto", confianca="alta"),
        _evento(2, "questao_objetiva", "incorreto", erros=("regra",), confianca="alta"),
        _evento(3, "questao_objetiva", "incorreto", erros=("regra",), confianca="alta"),
        _evento(
            4,
            "revisao_julgado",
            "correto",
            evidencias=("retencao_revisao_posterior",),
            confianca="media",
        ),
        _evento(5, "explicacao", "nao_avaliado", tentativa=False),
    ]

    relatorio = modulo.gerar_relatorio(
        eventos, (date(2026, 9, 1), date(2026, 9, 30))
    )

    assert relatorio["tentativas"] == 4
    assert relatorio["precisao_por_modalidade"]["questao_objetiva"] == {
        "tentativas": 3,
        "corretas": 1,
        "precisao": 1 / 3,
    }
    assert relatorio["reincidencia_erros"] == {"regra": 2}
    assert relatorio["retencao_observada"] == {
        "evidencias": 1,
        "sucessos": 1,
        "precisao": 1.0,
        "estado": "observada",
    }
    assert relatorio["calibracao_confianca"]["alta"]["corretas"] == 1
    assert relatorio["estado_evidencia"] == "evidencia_disponivel"
    assert not ({"ranking", "pontuacao_global", "previsao_aprovacao"} & relatorio.keys())


def test_relatorio_distingue_sem_evidencia_de_desempenho_insuficiente():
    modulo = _module()
    periodo = (date(2026, 9, 1), date(2026, 9, 30))
    sem_tentativa = [
        _evento(1, "explicacao", "nao_avaliado", tentativa=False)
    ]
    com_erro = [
        _evento(1, "questao_objetiva", "incorreto", erros=("conceito",))
    ]

    assert modulo.gerar_relatorio(sem_tentativa, periodo)["estado_evidencia"] == (
        "sem_evidencia"
    )
    assert modulo.gerar_relatorio(com_erro, periodo)["estado_evidencia"] == (
        "desempenho_insuficiente_observado"
    )


def test_cli_exige_formato_explicito_para_json_ou_markdown(tmp_path):
    entrada = tmp_path / "eventos.json"
    entrada.write_text(
        json.dumps([_evento(1, "questao_objetiva", "correto")]),
        encoding="utf-8",
    )
    comando = [
        sys.executable,
        str(SCRIPT),
        "--entrada",
        str(entrada),
        "--inicio",
        "2026-09-01",
        "--fim",
        "2026-09-30",
    ]

    sem_formato = subprocess.run(
        comando, capture_output=True, text=True, check=False
    )
    assert sem_formato.returncode != 0

    json_explicito = subprocess.run(
        [*comando, "--formato", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert json_explicito.returncode == 0
    assert json.loads(json_explicito.stdout)["tentativas"] == 1

