import preparar_itens_esteira as preparador
import pytest


def registro(identificador, estado="confirmado"):
    return {
        "id": identificador,
        "tema": "Tutela coletiva",
        "tribunal": "STJ",
        "disciplina": "Processo Civil",
        "estado": estado,
        "grau_confianca": "alto",
        "fontes_essenciais": "acórdão e informativo",
    }


def test_converter_preserva_metadados_exclui_superado_e_deduplica():
    itens, excluidos = preparador.converter(
        [registro("R-1"), registro("R-1"), registro("R-2", "superado")],
        altas=set(), erros={"R-1"}, motivos={}, incluir_superados=False,
    )

    assert excluidos == 1
    assert itens == [{
        "id": "R-1", "tema": "Tutela coletiva", "tribunal": "STJ",
        "disciplina": "Processo Civil", "estado_jurisprudencial": "confirmado",
        "grau_confianca": "alto", "fontes_essenciais": "acórdão e informativo",
        "prioridade": "padrao", "motivo_prioridade": "erro documentado", "origem_erro": "sim",
    }]


def test_prioridade_alta_exige_motivo_explicito():
    with pytest.raises(ValueError, match="prioridade alta exige"):
        preparador.converter([registro("R-3")], {"R-3"}, set(), {}, False)
