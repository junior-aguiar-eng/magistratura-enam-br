from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOLO = ROOT / "skills" / "acompanhar-percurso-magistratura" / "references" / "transicoes-inteligentes.md"


def test_protocolo_declara_as_sete_classes_de_transicao():
    texto = PROTOCOLO.read_text(encoding="utf-8")

    for classe in ("CONTINUAR", "MUDAR_TEMA", "MUDAR_MODALIDADE", "MUDAR_SKILL", "SUSPENDER", "RETOMAR", "ENCERRAR"):
        assert f"`{classe}`" in texto


def test_mudanca_inequivoca_flui_e_perda_material_exige_uma_decisao():
    texto = PROTOCOLO.read_text(encoding="utf-8")

    assert "comunicada em uma frase e prossegue na mesma resposta" in texto
    assert "Faça uma única pergunta de decisão somente quando" in texto
    assert "descartaria irreversivelmente uma atividade pendente" in texto
    assert "Se o candidato disser “abandone”, “encerre”, “substitua”" in texto
    assert "cumpra sem reconfirmar" in texto


def test_modalidade_preserva_tema_e_pendencia_nao_vira_desempenho():
    texto = PROTOCOLO.read_text(encoding="utf-8")

    assert "Preserve o tema" in texto
    assert "não trate a mudança como erro, tentativa ou abandono" in texto
    assert "Suspender, encerrar e substituir são atos distintos" in texto


def test_cinco_pendencias_materiais_possuem_tratamento_explicito():
    texto = PROTOCOLO.read_text(encoding="utf-8")

    for pendencia in ("Questão aguardando resposta", "Discursiva em elaboração", "Curadoria incompleta", "Comparação sem segundo documento", "Remediação aberta"):
        assert f"**{pendencia}:**" in texto


def test_retomada_entre_sessoes_exige_estado_fornecido():
    texto = PROTOCOLO.read_text(encoding="utf-8")

    assert "Pendência existe apenas na conversa atual" in texto
    assert "checkpoint, perfil ou evento local válido" in texto
    assert "não persista automaticamente" in texto
