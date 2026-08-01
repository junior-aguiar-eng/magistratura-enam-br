import json
import subprocess
import sys
from pathlib import Path

from auditar_rastreabilidade import TIPOS_CORRESPONDENCIA, auditar

AUDITOR = Path(__file__).resolve().parents[1] / "scripts" / "auditar_rastreabilidade.py"


def referencia(documento):
    return {"documento": documento, "pagina": "1", "localizacao": "Tema"}


def fundamento(tipo="LEGISLACAO"):
    return {
        "tipo": tipo,
        "identificador": "Lei 1/2026" if tipo == "LEGISLACAO" else "Tema 1/STF",
        "fonte_oficial": "Fonte oficial competente",
    }


def manifesto():
    return {
        "id_execucao": "enam-2025-2026-civil",
        "escopo": "Comparação teste",
        "documentos": [
            {"id": "anterior", "edicao": "2025", "arquivo": "anterior.pdf", "tipo_fonte": "material original"},
            {"id": "atual", "edicao": "2026", "arquivo": "atual.pdf", "tipo_fonte": "material original"},
        ],
    }


def item_mapeado(identificador="civil-01", tipo="CORRESPONDENCIA TEMATICA CONFIRMADA"):
    return {
        "id_item": identificador,
        "disciplina": "Direito Civil",
        "tema_subtema": "Obrigações",
        "referencias_anteriores": [referencia("anterior")],
        "referencias_atuais": [referencia("atual")],
        "tipo_correspondencia": tipo,
        "evidencias": [referencia("anterior")],
    }


def item_comparativo(identificador="civil-01", tipo="CORRESPONDENCIA TEMATICA CONFIRMADA"):
    return {
        "id_item": identificador,
        "disciplina": "Direito Civil",
        "tema_subtema": "Obrigações",
        "referencias_anteriores": [referencia("anterior")],
        "referencias_atuais": [referencia("atual")],
        "tipo_correspondencia": tipo,
        "classificacao": "SEM DELTA",
        "delta_real": "Sem alteração jurídica material.",
        "acao_recomendada": "SEM_ACAO",
        "evidencias": [referencia("atual")],
    }


def executar_auditoria(mapeados, comparativos):
    return auditar(
        manifesto(),
        {"id_execucao": "enam-2025-2026-civil", "escopo": "Comparação teste", "itens": mapeados},
        {"id_execucao": "enam-2025-2026-civil", "escopo": "Comparação teste", "itens": comparativos},
    )


def executar_auditoria_cli(tmp_path, manifesto_dados, mapeamento_dados, comparativo_dados):
    caminhos = {
        "manifesto": tmp_path / "manifesto.json",
        "mapeamento": tmp_path / "mapeamento.json",
        "comparativo": tmp_path / "comparativo.json",
    }
    for nome, dados in (("manifesto", manifesto_dados), ("mapeamento", mapeamento_dados), ("comparativo", comparativo_dados)):
        caminhos[nome].write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    resultado = subprocess.run(
        [sys.executable, str(AUDITOR), "--manifesto", str(caminhos["manifesto"]), "--mapeamento", str(caminhos["mapeamento"]), "--comparativo", str(caminhos["comparativo"])],
        capture_output=True,
        text=True,
        check=False,
    )
    return resultado, json.loads(resultado.stdout)


def artefatos(mapeados=None, comparativos=None):
    return (
        manifesto(),
        {"id_execucao": "enam-2025-2026-civil", "escopo": "Comparação teste", "itens": mapeados or [item_mapeado()]},
        {"id_execucao": "enam-2025-2026-civil", "escopo": "Comparação teste", "itens": comparativos or [item_comparativo()]},
    )


def test_auditoria_aprova_vinculo_completo():
    assert executar_auditoria([item_mapeado()], [item_comparativo()]) == []


def test_auditoria_rejeita_tipo_de_correspondencia_invalido():
    erros = executar_auditoria([item_mapeado(tipo="TIPO INVALIDO")], [item_comparativo(tipo="TIPO INVALIDO")])
    assert any("tipo_correspondencia não padronizado" in erro for erro in erros)


def test_auditoria_rejeita_delta_orfao():
    erros = executar_auditoria([item_mapeado()], [item_comparativo(identificador="inexistente")])
    assert any("id_item não existe no mapeamento" in erro for erro in erros)


def test_auditoria_exige_cobertura_do_mapeamento():
    erros = executar_auditoria([item_mapeado(), item_mapeado("civil-02")], [item_comparativo()])
    assert any("id_item sem delta correspondente: civil-02" in erro for erro in erros)


def test_vocabulos_do_schema_e_do_auditor_sao_iguais():
    schema = json.loads((Path(__file__).resolve().parents[1] / "modelos" / "mapeamento.schema.json").read_text(encoding="utf-8"))
    assert set(schema["$defs"]["item"]["properties"]["tipo_correspondencia"]["enum"]) == TIPOS_CORRESPONDENCIA


def test_auditoria_aplica_padrao_de_identificador_do_schema():
    erros = executar_auditoria([item_mapeado(identificador="civil 01")], [item_comparativo(identificador="civil 01")])
    assert any("schema inválido" in erro and "civil 01" in erro for erro in erros)


def test_auditoria_rejeita_propriedade_fora_do_schema():
    mapeado = item_mapeado()
    mapeado["campo_inventado"] = "não permitido"
    erros = executar_auditoria([mapeado], [item_comparativo()])
    assert any("schema inválido" in erro and "campo_inventado" in erro for erro in erros)


def test_auditoria_rejeita_execucao_divergente():
    mapeamento = {"id_execucao": "enam-2025-2026-civil", "escopo": "Comparação teste", "itens": [item_mapeado()]}
    comparativo = {"id_execucao": "enam-2024-2025-civil", "escopo": "Comparação teste", "itens": [item_comparativo()]}
    erros = auditar(manifesto(), mapeamento, comparativo)
    assert any("id_execucao diverge do manifesto" in erro for erro in erros)


def test_auditoria_rejeita_tema_divergente_do_mapeamento():
    comparativo = item_comparativo()
    comparativo["tema_subtema"] = "Contratos"
    erros = executar_auditoria([item_mapeado()], [comparativo])
    assert any("tema_subtema diverge do mapeamento" in erro for erro in erros)


def test_auditoria_rejeita_sem_delta_junto_a_delta_material():
    delta_material = item_comparativo()
    delta_material["classificacao"] = "ATUALIZACAO LEGISLATIVA"
    delta_material["delta_real"] = "Lei posterior alterou o regime aplicável."
    delta_material["acao_recomendada"] = "SUBSTITUIR"
    delta_material["fundamento_material"] = fundamento()
    erros = executar_auditoria([item_mapeado()], [item_comparativo(), delta_material])
    assert any("SEM DELTA deve ser exclusivo" in erro for erro in erros)


def test_auditoria_exige_referencias_bilaterais_para_delta_material():
    comparativo = item_comparativo()
    comparativo["classificacao"] = "ATUALIZACAO LEGISLATIVA"
    comparativo["delta_real"] = "Lei posterior alterou o regime aplicável."
    comparativo["acao_recomendada"] = "SUBSTITUIR"
    comparativo["fundamento_material"] = fundamento()
    comparativo["referencias_atuais"] = []
    erros = executar_auditoria([item_mapeado()], [comparativo])
    assert any("referencias_atuais: exige ao menos uma referência" in erro for erro in erros)


def test_auditoria_exige_fundamento_oficial_para_atualizacao_legislativa():
    comparativo = item_comparativo()
    comparativo["classificacao"] = "ATUALIZACAO LEGISLATIVA"
    comparativo["delta_real"] = "Lei posterior alterou o regime aplicável."
    comparativo["acao_recomendada"] = "SUBSTITUIR"
    erros = executar_auditoria([item_mapeado()], [comparativo])
    assert any("fundamento_material" in erro for erro in erros)


def test_auditoria_exige_tipo_compativel_com_atualizacao_jurisprudencial():
    comparativo = item_comparativo()
    comparativo["classificacao"] = "ATUALIZACAO JURISPRUDENCIAL"
    comparativo["delta_real"] = "Precedente posterior alterou a orientação aplicável."
    comparativo["acao_recomendada"] = "SUBSTITUIR"
    comparativo["fundamento_material"] = fundamento("LEGISLACAO")
    erros = executar_auditoria([item_mapeado()], [comparativo])
    assert any("JURISPRUDENCIA" in erro for erro in erros)


def test_pendente_de_publicacao_nao_exige_referencias_bilaterais():
    comparativo = item_comparativo()
    comparativo["classificacao"] = "PENDENTE DE PUBLICACAO"
    comparativo["delta_real"] = "Documento posterior ainda não foi publicado."
    comparativo["acao_recomendada"] = "AGUARDAR_PUBLICACAO"
    comparativo["referencias_anteriores"] = []
    comparativo["referencias_atuais"] = []
    assert executar_auditoria([item_mapeado()], [comparativo]) == []


def test_auditoria_rejeita_acao_incompativel_com_classificacao():
    comparativo = item_comparativo()
    comparativo["acao_recomendada"] = "INCLUIR"
    erros = executar_auditoria([item_mapeado()], [comparativo])
    assert any("acao_recomendada deve ser SEM_ACAO" in erro for erro in erros)


def test_auditoria_cli_aprova_fluxo_completo(tmp_path):
    resultado, saida = executar_auditoria_cli(tmp_path, *artefatos())
    assert resultado.returncode == 0
    assert saida == {"status": "aprovado", "erros": []}


def test_auditoria_cli_rejeita_limites_semanticos(tmp_path):
    casos = []

    manifesto_dados, mapeamento_dados, comparativo_dados = artefatos()
    comparativo_dados["escopo"] = "Outro recorte"
    casos.append(("escopo", manifesto_dados, mapeamento_dados, comparativo_dados, "escopo diverge do manifesto"))

    manifesto_dados, mapeamento_dados, comparativo_dados = artefatos()
    delta = item_comparativo()
    delta.update({
        "classificacao": "ATUALIZACAO LEGISLATIVA",
        "delta_real": "Lei posterior alterou o regime aplicável.",
        "acao_recomendada": "SUBSTITUIR",
        "fundamento_material": fundamento(),
    })
    comparativo_dados["itens"].append(delta)
    casos.append(("sem-delta", manifesto_dados, mapeamento_dados, comparativo_dados, "SEM DELTA deve ser exclusivo"))

    manifesto_dados, mapeamento_dados, comparativo_dados = artefatos()
    comparativo_dados["itens"][0].update({
        "classificacao": "ATUALIZACAO LEGISLATIVA",
        "delta_real": "Lei posterior alterou o regime aplicável.",
        "acao_recomendada": "SUBSTITUIR",
        "fundamento_material": fundamento(),
        "referencias_atuais": [],
    })
    casos.append(("prova-unilateral", manifesto_dados, mapeamento_dados, comparativo_dados, "referencias_atuais: exige ao menos uma referência"))

    manifesto_dados, mapeamento_dados, comparativo_dados = artefatos()
    comparativo_dados["itens"][0].update({
        "classificacao": "ATUALIZACAO LEGISLATIVA",
        "delta_real": "Lei posterior alterou o regime aplicável.",
        "acao_recomendada": "SUBSTITUIR",
    })
    casos.append(("fundamento-ausente", manifesto_dados, mapeamento_dados, comparativo_dados, "fundamento_material"))

    for nome, manifesto_dados, mapeamento_dados, comparativo_dados, mensagem in casos:
        diretorio = tmp_path / nome
        diretorio.mkdir()
        resultado, saida = executar_auditoria_cli(diretorio, manifesto_dados, mapeamento_dados, comparativo_dados)
        assert resultado.returncode == 2
        assert saida["status"] == "reprovado"
        assert any(mensagem in erro for erro in saida["erros"])
