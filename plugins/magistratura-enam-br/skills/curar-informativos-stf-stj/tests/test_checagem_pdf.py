from checar_estrutura_informativo import analisar


def pagina(texto, n=1, erro=""):
    return {"pagina": n, "texto": texto, "caracteres": len(texto.strip()), "erro_extracao": erro}


def test_pdf_sem_texto_e_reprovado():
    resultado = analisar([pagina("")])
    assert resultado["status"] == "reprovado"


def test_pdf_legivel_sem_cabecalho_tem_ressalva():
    resultado = analisar([pagina("1. " + "A" * 200)])
    assert resultado["status"] == "aprovado_com_ressalvas"
    assert not resultado["cabecalho_detectado"]


def test_pdf_legivel_aprovado():
    resultado = analisar([pagina("INFORMATIVO STF\n1. " + "A" * 200)])
    assert resultado["status"] == "aprovado"


def test_indicador_nao_e_contagem_definitiva():
    resultado = analisar([pagina("INFORMATIVO STJ\nREsp 1/RS " + "A" * 200)])
    assert "não constituem contagem definitiva" in resultado["nota"]
