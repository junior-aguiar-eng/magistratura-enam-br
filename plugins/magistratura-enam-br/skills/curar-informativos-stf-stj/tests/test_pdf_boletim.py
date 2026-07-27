from pathlib import Path
import pytest

from gerar_pdf_boletim import gerar, paragrafos, validar_dados


def dados_validos():
    return {
        "titulo_boletim": "Boletim & teste",
        "data_geracao": "2026-07-11",
        "nota_metodologica": "Leitura integral & triagem.",
        "julgados_stf": [{
            "titulo": "Tema <constitucional>",
            "comentario": "Texto com & e <tags>.",
            "estado_jurisprudencial": "confirmado",
            "grau_confianca": "alto",
            "data_verificacao": "2026-07-11",
            "fontes_essenciais": []
        }],
        "julgados_stj": [],
        "nao_selecionados": [],
        "pendencias": [],
        "fontes_essenciais": []
    }


def test_escape_de_markup():
    partes = paragrafos("A & B <script>alert(1)</script>")
    assert "&amp;" in partes[0] and "&lt;script&gt;" in partes[0]


def test_validacao_exige_nota_para_confianca_media():
    d = dados_validos()
    d["julgados_stf"][0]["grau_confianca"] = "médio"
    with pytest.raises(ValueError):
        validar_dados(d)


def test_gera_pdf_com_caracteres_especiais(tmp_path):
    saida = tmp_path / "boletim.pdf"
    gerar(validar_dados(dados_validos()), saida)
    assert saida.exists() and saida.stat().st_size > 500
