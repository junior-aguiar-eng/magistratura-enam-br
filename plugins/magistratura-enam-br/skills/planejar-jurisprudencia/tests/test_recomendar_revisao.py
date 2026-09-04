import pytest
from recomendar_revisao import recomendar_revisao


def evento(resultado, confianca, evidencias=(), motivos=()):
    return {
        "occurred_at": "2026-09-04T12:00:00Z",
        "performance": {
            "result": resultado,
            "confidence": confianca,
            "domain_evidence": list(evidencias),
        },
        "routing": {"reason_codes": list(motivos)},
    }


@pytest.mark.parametrize(
    ("entrada", "fixo", "esperado", "motivo"),
    [
        (evento("incorreto", "alta"), 21, 1, "incorrect"),
        (evento("parcial", "media"), 21, 3, "partial"),
        (evento("correto", None), 21, 21, "fixed_policy_preserved"),
        (evento("correto", "baixa", ("fundamentacao_normativa_jurisprudencial",)), 21, 21, "low_confidence"),
        (evento("correto", "alta"), 21, 21, "missing_justification"),
        (evento("correto", "alta", ("fundamentacao_normativa_jurisprudencial",)), 21, 26, "high_confidence_no_transfer"),
        (evento("correto", "alta", ("fundamentacao_normativa_jurisprudencial", "aplicacao_fatos_novos")), 75, 90, "high_confidence_with_transfer"),
        (evento("incorreto", "alta", motivos=("repeated_error",)), 21, 1, "repeated_error"),
    ],
)
def test_politica_adaptativa_v1(entrada, fixo, esperado, motivo):
    recomendacao = recomendar_revisao(entrada, fixo)

    assert recomendacao["suggested_interval_days"] == esperado
    assert motivo in recomendacao["reason_codes"]


def test_modo_sombra_preserva_data_efetiva():
    recomendacao = recomendar_revisao(
        evento("incorreto", "alta"), intervalo_fixo=21, modo_sombra=True
    )

    assert recomendacao["fixed_review_at"] == "2026-09-25"
    assert recomendacao["suggested_review_at"] == "2026-09-05"
    assert recomendacao["effective_review_at"] == recomendacao["fixed_review_at"]
    assert recomendacao["shadow_mode"] is True


@pytest.mark.parametrize("campo", ["result", "confidence", "domain_evidence"])
def test_rejeita_evidencia_exigida_ausente(campo):
    entrada = evento("correto", "alta", ("fundamentacao_normativa_jurisprudencial",))
    del entrada["performance"][campo]

    with pytest.raises(ValueError, match=campo):
        recomendar_revisao(entrada, 21)

