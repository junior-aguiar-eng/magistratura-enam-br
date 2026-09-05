from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ler(caminho):
    return (ROOT / caminho).read_text(encoding="utf-8")


def test_acervo_exclusivo_bloqueia_toda_consulta_externa():
    protocolo = ler("references/protocolo-uso-do-acervo.md")
    assert "Acervo exclusivo" in protocolo
    assert "Não navegue, pesquise, complete por memória externa nem consulte fonte oficial" in protocolo
    assert "não posso certificar a atualização externa deste ponto" in protocolo


def test_validacao_oficial_e_proporcional_e_primaria():
    protocolo = ler("references/protocolo-uso-do-acervo.md")
    assert "apenas quando atualidade ou precisão puderem alterar materialmente a conclusão" in protocolo
    assert "Não faça pesquisa exploratória ou editorial" in protocolo


def test_pesquisa_completa_comeca_na_fonte_primaria():
    protocolo = ler("references/protocolo-uso-do-acervo.md")
    assert "Consulte primeiro a fonte primária aplicável" in protocolo
    assert "Planalto para legislação federal" in protocolo
    assert "STF ou STJ para seus julgados" in protocolo


def test_preferencia_inferida_nao_vira_perfil_persistente():
    protocolo = ler("references/protocolo-uso-do-acervo.md")
    agents = ler("AGENTS.md")
    assert "válida somente na conversa atual" in protocolo
    assert "nunca perfil persistente" in agents


def test_apresentacao_e_rastreavel_sem_clipping():
    protocolo = ler("references/protocolo-uso-do-acervo.md")
    diretrizes = ler("references/diretrizes-estudo-juridico-brasileiro.md")
    assert "Base consultada" in protocolo
    assert "evite URL bruta no corpo" in protocolo
    assert "não transforme a resposta em clipping" in diretrizes.lower()
    assert "sem ocultar citações automáticas" in protocolo


def test_fonte_editorial_nao_substitui_documento_oficial():
    diretrizes = ler("references/diretrizes-estudo-juridico-brasileiro.md")
    assert "Notícia de julgamento, resumo editorial ou comentário doutrinário não comprovam" in diretrizes
    assert "fontes editoriais secundárias, nunca como autoridade oficial" in diretrizes
