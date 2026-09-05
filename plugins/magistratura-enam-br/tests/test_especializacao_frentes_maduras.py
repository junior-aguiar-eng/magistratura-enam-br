def test_curadoria_preserva_campos_e_evita_burocracia(texto):
    referencia = texto("skills/curar-informativos-stf-stj/references/comentario-jurisprudencial.md").casefold()
    for campo in (
        "tese",
        "contexto",
        "fundamento determinante",
        "alcance",
        "limites",
        "distinções",
        "situação processual",
    ):
        assert campo in referencia
    assert "proporcional" in referencia
    assert "inferência" in referencia
    assert "parágrafo burocrático" in referencia


def test_planejamento_nao_cristaliza_evidencia_historica(texto):
    politica = texto("skills/planejar-jurisprudencia/references/politica-adaptativa-v1.md").casefold()
    assert "assistência" in politica
    assert "transferência" in politica
    assert "retenção" in politica
    assert "não cristaliza" in politica


def test_comparacao_distingue_tres_classes_de_mudanca(texto):
    formato = texto("skills/comparar-materiais-enam/references/formato-entrega-comparativo.md").casefold()
    for classe in ("ausência aparente", "mudança editorial", "alteração jurídica"):
        assert classe in formato
    assert "ação de estudo" in formato
