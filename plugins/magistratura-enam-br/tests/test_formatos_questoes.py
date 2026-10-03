"""Contratos de instrução: não certificam validade jurídica de questões geradas."""

import pytest


@pytest.mark.parametrize("formato", ["direto", "numerado", "vf", "associacao"])
def test_vocabulario_de_formatos_e_compartilhado_sem_novo_campo_mcp(texto, formato):
    for caminho in (
        "skills/estudar-direito-magistratura/SKILL.md",
        "skills/estudar-direito-magistratura/references/questoes-fgv-enam.md",
        "references/questoes-interativas-mcp.md",
    ):
        assert f"`{formato}`" in texto(caminho)
    integration = texto("references/questoes-interativas-mcp.md")
    assert "sem novo campo obrigatório" in integration
    assert "prompt e nas cinco alternativas" in integration


@pytest.mark.parametrize("desenho", ["solucoes", "matriz", "fundamento"])
def test_desenhos_sao_orientacoes_sem_quotas_ou_inferencia_de_dominio(texto, desenho):
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")
    assert f"`{desenho}`" in referencia
    assert "não são evidência de desempenho ou domínio" in referencia
    assert "Não imponha porcentagens" in referencia
    assert "uma questão única" in referencia


def test_combinacoes_exigem_unicidade_e_correcao_por_item(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md")
    assert "duas alternativas com a mesma combinação" in referencia
    assert "cada assertiva e cada associação" in referencia
    assert "somente após a tentativa" in referencia
    assert "O acerto não dispensa" in referencia


def test_cenarios_separam_pedido_rubrica_e_aprovacao_humana(texto):
    cenarios = texto("skills/estudar-direito-magistratura/references/cenarios-avaliacao.md")
    for numero in range(11, 18):
        assert f"## Q{numero} —" in cenarios
    for criterio in (
        "suporte oficial/material",
        "núcleo funcional",
        "plausibilidade",
        "unicidade",
        "comparação dos distratores",
        "limite de fonte",
    ):
        assert criterio in cenarios
    assert "candidata pendente de revisão humana" in cenarios
    assert "não forneça a rubrica" in cenarios
