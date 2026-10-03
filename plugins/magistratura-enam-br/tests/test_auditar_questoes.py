"""Auditoria estrutural/editorial; fixtures não representam prova ou mérito jurídico."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def auditor():
    script = ROOT / "scripts/auditar_questoes.py"
    assert script.is_file(), "Auditor quantitativo ausente"
    import auditar_questoes

    return auditar_questoes


def bloco(identifier="1", prompt="Assinale a alternativa correta.", labels="ABCDE"):
    return f"## Questão {identifier} — Tema sintético\n{prompt}\n" + "\n".join(
        f"{letter}) Solução {letter} com requisito e consequência delimitados."
        for letter in labels
    )


def questao(auditor, identifier="q1", *, longest="C", absolutes=False):
    options = []
    for letter in "ABCDE":
        text = "A regra depende dos pressupostos indicados."
        if letter == longest:
            text += (
                " A consequência considera também o limite explicitamente delimitado."
            )
        if absolutes and letter != "C":
            text += " Sempre em qualquer caso, sem exceção."
        options.append((letter, text))
    return auditor.AuditQuestion(
        identifier, "direto", "Um caso com dois planos decisivos.", options
    )


def codes(result, field="errors"):
    return {entry["code"] for entry in result[field]}


def test_parser_preserva_cinco_a_para_rejeicao_sem_colapsar_lista(auditor):
    parsed = auditor.parse_question_block(bloco(labels="AAAAA"), format="markdown")
    assert [label for label, _ in parsed[0].alternatives] == list("AAAAA")
    assert "alternative_labels" in codes(auditor.audit_question_block(parsed))


@pytest.mark.parametrize("labels", ["ABCD", "ABCDF", "ABCDEE", "ABCDEA"])
def test_alternativas_ausentes_extras_ou_repetidas_impedem_aprovacao(auditor, labels):
    result = auditor.audit_question_block(
        auditor.parse_question_block(bloco(labels=labels), format="markdown")
    )
    assert "alternative_labels" in codes(result)
    assert result["status"] == "reprovado_estruturalmente"


def test_ids_duplicados_nao_recebem_chave_por_colisao(auditor):
    parsed = auditor.parse_question_block(
        bloco("1") + "\n" + bloco("1"), format="markdown"
    )
    result = auditor.audit_question_block(parsed, {"1": "C"})
    assert "duplicate_id" in codes(result)
    assert result["metrics"]["answer_distribution"]["sample_size"] == 0


@pytest.mark.parametrize("answer", ["F", "c", "", 1, None])
def test_chave_incompativel_nao_entra_em_distribuicao(auditor, answer):
    result = auditor.audit_question_block([questao(auditor)], {"q1": answer})
    assert "invalid_answer" in codes(result)
    assert result["metrics"]["answer_distribution"]["sample_size"] == 0


def test_chaves_interna_e_externa_contraditorias_nao_vazam_valores(auditor):
    question = questao(auditor)
    question.correct_option = "B"
    result = auditor.audit_question_block([question], {"q1": "C"})
    assert "contradictory_answer" in codes(result)
    assert result["metrics"]["answer_distribution"]["sample_size"] == 0
    assert "correct_option" not in json.dumps(result)


@pytest.mark.parametrize("format,text", [("markdown", ""), ("json", "[]")])
def test_bloco_vazio_reprovado(auditor, format, text):
    result = auditor.audit_question_block(
        auditor.parse_question_block(text, format=format)
    )
    assert "empty_block" in codes(result)


@pytest.mark.parametrize(
    "text", ["Texto sem questões", "## Questão 1\n", "```python\nprint(1)\n```"]
)
def test_markdown_nao_interpretavel_falha_explicitamente(auditor, text):
    with pytest.raises(ValueError):
        auditor.parse_question_block(text, format="markdown")


@pytest.mark.parametrize(
    "payload",
    [
        {},
        [1],
        [{"session_id": "q1", "prompt": 1, "alternatives": []}],
        [{"session_id": "q1", "prompt": "Texto", "alternatives": {"A": "x"}}],
    ],
)
def test_json_nao_interpretavel_falha_explicitamente(auditor, payload):
    with pytest.raises(ValueError):
        auditor.parse_question_block(json.dumps(payload), format="json")


def test_json_duplicado_nao_perde_gabarito_contraditorio_no_decoder(auditor):
    with pytest.raises(ValueError):
        auditor.parse_question_block(
            '[{"session_id":"q1","session_id":"q2"}]', format="json"
        )


def test_json_projecao_existente_e_gabarito_privado_opcional(auditor):
    from test_mcp_question_sessions import sessao

    parsed = auditor.parse_question_block(json.dumps([sessao()]), format="json")
    assert parsed[0].id == "qsn_0123456789abcdef"
    assert parsed[0].correct_option == "C"
    result = auditor.audit_question_block(parsed)
    assert result["status"] == "aprovado_estruturalmente"
    assert result["metrics"]["answer_distribution"]["counts"]["C"] == 1
    assert "juridical_merit" in codes(result, "not_checked")


def test_json_opcoes_duplicadas_preservadas(auditor):
    payload = [
        {
            "session_id": "q1",
            "prompt": "Assinale a correta.",
            "alternatives": [{"id": "A", "text": "Solução"}] * 5,
        }
    ]
    parsed = auditor.parse_question_block(json.dumps(payload), format="json")
    assert len(parsed[0].alternatives) == 5
    assert "alternative_labels" in codes(auditor.audit_question_block(parsed))


@pytest.mark.parametrize(
    "prompt,expected",
    [
        (
            "I. Primeira assertiva\ncontinua na linha seguinte.\nII. Segunda assertiva.\nIII. Terceira.\nQuais estão corretas?",
            "numerado",
        ),
        (
            "Assinale V para verdadeiro e F para falso.\nI. Situação.\nII. Outra.\nIII. Última.",
            "vf",
        ),
        (
            "Coluna I — situações\nI. Primeira.\nII. Segunda.\nColuna II — soluções\n1. Uma.\n2. Outra.\nAssocie as colunas.",
            "associacao",
        ),
        (
            "O juiz deve considerar regra e exceção. Assinale a alternativa correta.",
            "direto",
        ),
    ],
)
def test_formatos_e_assertivas_multilinha_preservados(auditor, prompt, expected):
    parsed = auditor.parse_question_block(bloco(prompt=prompt), format="markdown")
    assert parsed[0].format == expected
    assert parsed[0].prompt == prompt
    assert len(parsed[0].alternatives) == 5


def test_markdown_estilizado_e_continuacao_de_alternativa(auditor):
    text = "# **Questão 7 — Tema**\nCaso delimitado.\n" + "\n".join(
        f"- **{label})** Solução {label}.\n    Com consequência e requisito."
        for label in "ABCDE"
    )
    parsed = auditor.parse_question_block(text, format="markdown")
    assert parsed[0].id == "7"
    assert [label for label, _ in parsed[0].alternatives] == list("ABCDE")
    assert all("Com consequência" in option for _, option in parsed[0].alternatives)


@pytest.mark.parametrize(
    "leak",
    [
        "Gabarito: C",
        "Resposta correta: letra B",
        "Alternativa correta é D",
        "**Gabarito: A**",
    ],
)
def test_solucao_explicita_e_erro_estrutural(auditor, leak):
    result = auditor.audit_question_block(
        auditor.parse_question_block(bloco() + "\n" + leak, format="markdown")
    )
    assert "answer_leak" in codes(result)


def test_comando_assinale_a_correta_nao_e_vazamento(auditor):
    result = auditor.audit_question_block(
        auditor.parse_question_block(bloco(), format="markdown"), {"1": "C"}
    )
    assert not result["errors"]
    assert result["status"] == "aprovado_estruturalmente"


def test_sem_gabarito_e_parcial_sem_denominador_ficticio(auditor):
    result = auditor.audit_question_block([questao(auditor)])
    assert result["status"] == "checagem_parcial"
    assert "answer_coverage" in codes(result, "not_checked")
    assert result["metrics"]["answer_distribution"]["sample_size"] == 0
    assert result["metrics"]["length_pattern"]["denominator"] == 0


def test_gabarito_parcial_conta_so_itens_elegiveis(auditor):
    result = auditor.audit_question_block(
        [questao(auditor, f"q{i}") for i in range(3)], {"q0": "C"}
    )
    assert result["status"] == "checagem_parcial"
    assert result["metrics"]["answer_distribution"]["denominator"] == 1
    assert result["metrics"]["answer_coverage"] == {"sample_size": 1, "denominator": 3}
    assert not result["errors"]


def test_gabarito_orfao_e_erro(auditor):
    assert "unknown_answer_id" in codes(
        auditor.audit_question_block([questao(auditor)], {"outro": "C"})
    )


@pytest.mark.parametrize(
    "count,matches,warn", [(7, 7, False), (8, 6, False), (8, 7, True)]
)
def test_limite_agregado_de_extensao_e_absolutos(auditor, count, matches, warn):
    questions = [
        questao(
            auditor, f"q{i}", longest="C" if i < matches else "A", absolutes=i < matches
        )
        for i in range(count)
    ]
    result = auditor.audit_question_block(
        questions, {f"q{i}": "C" for i in range(count)}
    )
    assert ("length_pattern" in codes(result, "warnings")) is warn
    assert ("absolute_pattern" in codes(result, "warnings")) is warn
    assert result["metrics"]["length_pattern"]["sample_size"] == matches
    assert result["metrics"]["length_pattern"]["denominator"] == count
    assert not result["errors"]


def test_mede_todas_alternativas_inclusive_sem_chave(auditor):
    result = auditor.audit_question_block([questao(auditor)])
    sizes = result["metrics"]["alternative_lengths"]
    assert sizes["sample_size"] == 5
    assert len(sizes["items"]) == 5
    assert all(item["characters"] > 0 and item["words"] > 0 for item in sizes["items"])
    assert "format_calibration" in codes(result, "not_checked")


def test_letras_sequenciais_so_produzem_aviso(auditor):
    questions = [questao(auditor, f"q{i}") for i in range(4)]
    result = auditor.audit_question_block(questions, {f"q{i}": "B" for i in range(4)})
    assert "repeated_key_run" in codes(result, "warnings")
    assert not result["errors"]


def test_perfil_arbitrario_nao_certifica_corpus_ou_impoe_quota(auditor):
    result = auditor.audit_question_block(
        [questao(auditor)], profile={"format_distribution": {"vf": 1}}
    )
    assert "profile_not_validated" in codes(result, "not_checked")
    assert not result["errors"]


def test_formato_desconhecido_e_erro(auditor):
    question = questao(auditor)
    question.format = "discursivo"
    assert "unsupported_question_format" in codes(
        auditor.audit_question_block([question])
    )


@pytest.mark.parametrize("answers", [None, {"q1": "C"}, {"q1": "F"}])
def test_resultado_valida_schema_sem_texto_ou_gabarito_individual(auditor, answers):
    result = auditor.audit_question_block([questao(auditor)], answers)
    schema = json.loads(
        (ROOT / "modelos/pedagogia/question-block-audit.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema).validate(result)
    output = json.dumps(result, ensure_ascii=False)
    assert "Um caso com dois planos" not in output
    assert "A regra depende" not in output
    assert "correct_option" not in output


def cli(tmp_path, text, *, answers=None, profile=None, format="markdown"):
    source = tmp_path / "questoes.txt"
    source.write_text(text, encoding="utf-8")
    paths = [source]
    command = [
        sys.executable,
        "-B",
        str(ROOT / "scripts/auditar_questoes.py"),
        "--questoes",
        str(source),
        "--formato",
        format,
    ]
    for label, value in (("gabarito", answers), ("perfil", profile)):
        if value is not None:
            path = tmp_path / f"{label}.json"
            path.write_text(
                value if isinstance(value, str) else json.dumps(value), encoding="utf-8"
            )
            paths.append(path)
            command.extend([f"--{label}", str(path)])
    before = {path.name: path.read_bytes() for path in paths}
    process = subprocess.run(
        command, capture_output=True, encoding="utf-8", check=False
    )
    assert {path.name: path.read_bytes() for path in paths} == before
    assert set(before) == {path.name for path in tmp_path.iterdir()}
    return process, json.loads(process.stdout)


def test_cli_somente_leitura_com_gabarito_e_perfil(tmp_path, auditor):
    process, result = cli(tmp_path, bloco(), answers={"1": "C"}, profile={})
    assert process.returncode == 0
    assert result["questions_count"] == 1
    assert "profile_not_validated" in codes(result, "not_checked")


@pytest.mark.parametrize(
    "text,format,answers",
    [
        ("", "markdown", None),
        ("texto sem opções", "markdown", None),
        ('[{"session_id":"q1","session_id":"q2"}]', "json", None),
        (bloco(), "markdown", '{"1":"A","1":"B"}'),
    ],
)
def test_cli_erro_e_json_sem_mutar_entradas(tmp_path, auditor, text, format, answers):
    process, result = cli(tmp_path, text, format=format, answers=answers)
    assert process.returncode == 2
    assert result["status"] == "reprovado_estruturalmente"
    assert result["errors"]


def test_schema_impede_aprovacao_quando_ha_erro_ou_chave_incompleta(auditor):
    schema = json.loads(
        (ROOT / "modelos/pedagogia/question-block-audit.schema.json").read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(schema)
    for answers in (None, {"q1": "F"}):
        result = auditor.audit_question_block([questao(auditor)], answers)
        result["status"] = "aprovado_estruturalmente"
        assert list(validator.iter_errors(result)), (
            "Schema aceitou aprovação contraditória"
        )


def test_ordem_de_opcoes_nao_e_reescrita(auditor):
    question = questao(auditor)
    question.alternatives.reverse()
    original = list(question.alternatives)
    result = auditor.audit_question_block([question], {"q1": "C"})
    assert not result["errors"]
    assert question.alternatives == original


def test_chave_invalida_interrompe_sequencia_e_exclui_amostra(auditor):
    result = auditor.audit_question_block(
        [questao(auditor, f"q{i}") for i in range(5)],
        {"q0": "C", "q1": "C", "q3": "C", "q4": "C"},
    )
    assert "repeated_key_run" not in codes(result, "warnings")
    assert result["metrics"]["key_runs"]["longest_run"] == 2


def test_alternativas_empatadas_nao_contam_como_correta_mais_longa(auditor):
    question = questao(auditor)
    question.alternatives = [(label, "Extensão igual.") for label in "ABCDE"]
    result = auditor.audit_question_block([question], {"q1": "C"})
    assert result["metrics"]["length_pattern"]["sample_size"] == 0


@pytest.mark.parametrize(
    "tail",
    ["## Correção\nUma explicação sem letra.", "## Justificativa\nTexto posterior."],
)
def test_secao_posterior_nao_vira_texto_da_alternativa_e(auditor, tail):
    with pytest.raises(ValueError):
        auditor.parse_question_block(bloco() + "\n" + tail, format="markdown")


def test_nenhum_item_omitido_por_cabecalho_vazio_intermediario(auditor):
    with pytest.raises(ValueError):
        auditor.parse_question_block(
            "## Questão 1\n## Questão 2\nCaso.\n"
            + "\n".join(f"{label}) Solução." for label in "ABCDE"),
            format="markdown",
        )


@pytest.mark.parametrize("value", ["[]", "null", '{"x":NaN}'])
def test_gabarito_ou_perfil_nao_objeto_rejeitado_por_cli(tmp_path, auditor, value):
    process, result = cli(tmp_path, bloco(), profile=value)
    assert process.returncode == 2
    assert result["errors"]


def test_vf_reconhecido_pelas_sequencias_sem_palavra_no_comando(auditor):
    text = (
        "## Questão 1\nI. Primeira.\nII. Segunda.\nIII. Terceira.\nAs assertivas são, respectivamente:\n"
        + "\n".join(
            f"{label}) {sequence}."
            for label, sequence in zip(
                "ABCDE", ("V–V–F", "F–V–V", "V–F–V", "F–F–V", "V–F–F"), strict=True
            )
        )
    )
    assert auditor.parse_question_block(text, format="markdown")[0].format == "vf"


def test_markdown_malformado_nao_aproveita_cabecalho_como_enunciado(auditor):
    with pytest.raises(ValueError):
        auditor.parse_question_block(
            "## Questão 1\n" + "\n".join(f"{letter}) Opção." for letter in "ABCDE"),
            format="markdown",
        )


@pytest.mark.parametrize("marker", ["Resposta: C", "Solução: letra A"])
def test_marcador_simples_de_solucao_tambem_e_vazamento(auditor, marker):
    result = auditor.audit_question_block(
        auditor.parse_question_block(bloco() + "\n" + marker, format="markdown")
    )
    assert "answer_leak" in codes(result)


def test_cabecalho_indentado_e_continuacao_da_alternativa(auditor):
    text = (
        bloco() + "\n    Questão adicional mencionada apenas como exemplo da opção E."
    )
    parsed = auditor.parse_question_block(text, format="markdown")
    assert len(parsed) == 1
    assert "Questão adicional" in parsed[0].alternatives[-1][1]


@pytest.mark.parametrize("marker", ["Gabarito: C", "Resposta correta: letra B"])
def test_solucao_no_titulo_nao_e_descartada(tmp_path, auditor, marker):
    text = bloco().replace("Tema sintético", marker)
    process, result = cli(tmp_path, text, answers={"1": "C"})
    assert process.returncode == 2
    assert result["status"] == "reprovado_estruturalmente"


@pytest.mark.parametrize(
    "text",
    [
        "Assinale a alternativa correta e a respectiva fundamentação.",
        "A solução é a anulação do ato administrativo.",
    ],
)
def test_artigo_e_conjuncao_nao_sao_letra_de_gabarito(auditor, text):
    question = questao(auditor)
    question.prompt = text
    question.alternatives[0] = ("A", text)
    result = auditor.audit_question_block([question], {"q1": "C"})
    assert not result["errors"]
    assert result["status"] == "aprovado_estruturalmente"


@pytest.mark.parametrize("title", ["**Correção**", "__Justificativa__", "Correção:"])
def test_secao_de_solucao_estilizada_nao_integra_alternativa(auditor, title):
    with pytest.raises(ValueError):
        auditor.parse_question_block(
            bloco()
            + "\n"
            + title
            + "\nA opção C é a única correta porque satisfaz os requisitos.",
            format="markdown",
        )


def test_continuacao_com_palavra_correcao_permanece_na_opcao(auditor):
    continuation = "Correção do cadastro depende da comprovação dos requisitos."
    parsed = auditor.parse_question_block(
        bloco() + "\n" + continuation, format="markdown"
    )
    assert parsed[0].alternatives[-1][1].endswith(continuation)


@pytest.mark.parametrize(
    "marker", ["A alternativa correta é C.", "Gabarito: C — justificativa posterior."]
)
def test_letra_explicita_antes_de_pontuacao_continua_detectada(auditor, marker):
    question = questao(auditor)
    question.prompt = marker
    assert "answer_leak" in codes(auditor.audit_question_block([question]))
