"""Registros inteiramente sintéticos; nenhum resultado é estatística do ENAM."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def calibration():
    assert (ROOT / "scripts/calibrar_provas.py").is_file(), "Calibrador ausente"
    import calibrar_provas

    return calibrar_provas


def review(identifier="r1", format="direto", discipline="Constitucional"):
    return {
        "id": identifier,
        "reviewer": "Revisor fictício",
        "date": "2026-10-03",
        "note": "Classificação sintética para teste de contrato, sem aprovação real.",
        "format": format,
        "discipline": discipline,
        "point_source": {"type": "legislacao", "reference": "Dispositivo fictício"},
        "difficulty": {
            "label": "alta",
            "author": "Autor fictício",
            "method": "Articulação editorial de requisitos e consequências",
        },
    }


def corpus(*, evidence_kind="synthetic"):
    return {
        "schema_version": "1.0.0",
        "corpus_id": "teste-caderno",
        "evidence_kind": evidence_kind,
        "edition": "Edição fictícia",
        "exam_type": "enam",
        "date": "2026-10-01",
        "expected_questions": 4,
        "official_source": {
            "url": "https://conhecimento.fgv.br/fixture-inexistente.pdf",
            "sha256": "a" * 64,
            "accessed_at": "2026-10-03",
        },
        "document_review": {
            "reviewer": "Revisor fictício",
            "date": "2026-10-03",
            "note": "Fixture sintética, sem consulta documental real",
        },
        "answer_key": {
            "status": "definitivo",
            "url": "https://conhecimento.fgv.br/fixture-chave-inexistente.pdf",
            "sha256": "b" * 64,
        },
        "questions": [
            {"id": "1", "status": "valida", "reviews": [review()]},
            {
                "id": "2",
                "status": "valida",
                "reviews": [review(format="vf", discipline="Civil")],
            },
            {"id": "3", "status": "anulada", "reviews": [review(format="associacao")]},
            {"id": "4", "status": "valida", "reviews": []},
        ],
    }


def test_cobertura_e_distribuicao_excluem_anulada_e_nao_revisada(calibration):
    data = corpus()
    before = copy.deepcopy(data)
    profile = calibration.build_calibration_profile(data)
    assert data == before
    assert profile["coverage"] == {
        "expected": 4,
        "registered": 4,
        "reviewed": 3,
        "eligible": 2,
        "excluded": 2,
        "missing": 0,
    }
    assert profile["distributions"]["formats"] == {
        "sample_size": 2,
        "denominator": 2,
        "counts": {"direto": 1, "numerado": 0, "vf": 1, "associacao": 0},
    }
    assert profile["distributions"]["disciplines"]["counts"] == {
        "Constitucional": 1,
        "Civil": 1,
    }
    assert profile["distributions"]["point_sources"]["counts"] == {"legislacao": 2}
    assert {item["question_id"] for item in profile["exclusions"]} == {"3", "4"}
    assert profile["empirical_reference_available"] is False
    assert profile["status"] == "parcial"


@pytest.mark.parametrize(
    "path",
    [
        ("official_source",),
        ("official_source", "sha256"),
        ("document_review",),
        ("edition",),
    ],
)
def test_registro_documental_incompleto_e_rejeitado(calibration, path):
    data = corpus()
    target = data
    for part in path[:-1]:
        target = target[part]
    del target[path[-1]]
    with pytest.raises(ValueError):
        calibration.build_calibration_profile(data)


@pytest.mark.parametrize(
    "url",
    [
        "http://conhecimento.fgv.br/prova.pdf",
        "https://conhecimento.fgv.br.evil.test/prova.pdf",
        "https://site-privado.test/prova.pdf",
        "https://usuario:senha@conhecimento.fgv.br/prova.pdf",
    ],
)
def test_origem_nao_oficial_ou_ambigua_e_rejeitada(calibration, url):
    data = corpus()
    data["official_source"]["url"] = url
    with pytest.raises(ValueError):
        calibration.validate_corpus(data)


@pytest.mark.parametrize("status", ["provisorio", "ausente"])
def test_gabarito_nao_definitivo_impede_todas_distribuicoes(calibration, status):
    data = corpus()
    data["answer_key"] = {"status": status}
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["eligible"] == 0
    assert profile["distributions"]["formats"]["sample_size"] == 0
    assert profile["status"] == "sem_calibracao"
    assert len(profile["exclusions"]) == 4
    assert all(
        "answer_key_not_final" in item["reasons"] for item in profile["exclusions"]
    )


def test_gabarito_definitivo_exige_origem_e_hash(calibration):
    data = corpus()
    data["answer_key"] = {"status": "definitivo"}
    with pytest.raises(ValueError):
        calibration.validate_corpus(data)


@pytest.mark.parametrize("field", ["reviewer", "date", "note"])
def test_revisao_sem_identificacao_data_ou_nota_nao_e_aceita(calibration, field):
    data = corpus()
    del data["questions"][0]["reviews"][0][field]
    with pytest.raises(ValueError):
        calibration.validate_corpus(data)


@pytest.mark.parametrize("field", ["format", "discipline", "point_source"])
def test_classificacao_incompleta_e_exclusao_visivel(calibration, field):
    data = corpus()
    data["questions"][0]["reviews"][0][field] = None
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["eligible"] == 1
    assert "classification_incomplete" in profile["exclusions"][0]["reasons"]


def test_divergencia_nao_e_resolvida_por_media_ou_ultima_revisao(calibration):
    data = corpus()
    data["questions"][0]["reviews"].append(review("r2", "numerado"))
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["eligible"] == 1
    assert "classification_unresolved" in profile["exclusions"][0]["reasons"]
    assert len(profile["corpus"]["questions"][0]["reviews"]) == 2
    assert profile["distributions"]["formats"]["counts"]["numerado"] == 0


def test_resolucao_identificada_seleciona_revisao_sem_apagar_divergencia(calibration):
    data = corpus()
    question = data["questions"][0]
    question["reviews"].append(review("r2", "numerado"))
    question["resolution"] = {
        "selected_review_id": "r2",
        "reviewer": "Árbitro fictício",
        "date": "2026-10-03",
        "note": "Escolha editorial documentada",
    }
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["eligible"] == 2
    assert profile["distributions"]["formats"]["counts"]["numerado"] == 1
    assert len(profile["corpus"]["questions"][0]["reviews"]) == 2


@pytest.mark.parametrize(
    "change",
    [
        "duplicate_id",
        "duplicate_review",
        "unknown_selection",
        "invalid_date",
        "extra_response",
        "overcoverage",
    ],
)
def test_registro_ambiguo_invalido_ou_pessoal_falha(calibration, change):
    data = corpus()
    match change:
        case "duplicate_id":
            data["questions"][1]["id"] = "1"
        case "duplicate_review":
            data["questions"][0]["reviews"].append(review())
        case "unknown_selection":
            data["questions"][0]["resolution"] = {
                "selected_review_id": "ausente",
                "reviewer": "Teste",
                "date": "2026-10-03",
                "note": "Teste",
            }
        case "invalid_date":
            data["questions"][0]["reviews"][0]["date"] = "2026-02-30"
        case "extra_response":
            data["questions"][0]["candidate_response"] = "C"
        case "overcoverage":
            data["expected_questions"] = 3
    with pytest.raises(ValueError):
        calibration.validate_corpus(data)


def test_questoes_nao_cadastradas_constam_na_cobertura(calibration):
    data = corpus()
    data["expected_questions"] = 6
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["missing"] == 2
    assert profile["coverage"]["registered"] == 4
    assert profile["coverage"]["expected"] == 6


def test_corpus_vazio_nao_cria_estatistica(calibration):
    data = corpus()
    data["questions"] = []
    profile = calibration.build_calibration_profile(data)
    assert profile["status"] == "sem_calibracao"
    assert profile["distributions"]["formats"]["denominator"] == 0
    assert profile["coverage"]["missing"] == 4


@pytest.mark.parametrize("field", ["author", "method"])
def test_dificuldade_editorial_exige_autor_e_metodo(calibration, field):
    data = corpus()
    del data["questions"][0]["reviews"][0]["difficulty"][field]
    with pytest.raises(ValueError):
        calibration.validate_corpus(data)


def test_dificuldade_ausente_nao_e_inferida_de_disciplina(calibration):
    data = corpus()
    data["questions"][0]["reviews"][0]["difficulty"] = None
    profile = calibration.build_calibration_profile(data)
    assert profile["distributions"]["difficulty"]["denominator"] == 1
    assert profile["distributions"]["difficulty"]["counts"] == {"alta": 1}
    assert len(profile["difficulty_estimates"]) == 1
    assert profile["difficulty_estimates"][0]["author"] == "Autor fictício"
    assert "accuracy_not_measured" in profile["not_checked"]


def test_perfil_recomputavel_rejeita_contagens_adulteradas(calibration):
    profile = calibration.build_calibration_profile(corpus())
    calibration.validate_calibration_profile(profile)
    profile["distributions"]["formats"]["counts"]["vf"] = 99
    with pytest.raises(ValueError):
        calibration.validate_calibration_profile(profile)


def test_hash_de_registro_e_origens_sao_rastreaveis(calibration):
    data = corpus()
    profile = calibration.build_calibration_profile(data)
    assert len(profile["corpus_sha256"]) == 64
    assert profile["origin"]["edition"] == "Edição fictícia"
    assert profile["origin"]["exam_type"] == "enam"
    assert profile["origin"]["official_source"] == data["official_source"]
    reordered = dict(reversed(list(data.items())))
    assert (
        calibration.build_calibration_profile(reordered)["corpus_sha256"]
        == profile["corpus_sha256"]
    )


def test_schema_do_corpus_validado_antes_de_gerar_perfil(calibration):
    schema = json.loads(
        (ROOT / "modelos/pedagogia/exam-corpus.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(corpus())
    data = corpus()
    data["questions"][0]["reviews"][0]["format"] = "desconhecido"
    with pytest.raises(ValueError):
        calibration.build_calibration_profile(data)


def run_cli(tmp_path, text):
    path = tmp_path / "corpus.json"
    path.write_text(text, encoding="utf-8")
    before = path.read_bytes()
    process = subprocess.run(
        [
            sys.executable,
            "-B",
            str(ROOT / "scripts/calibrar_provas.py"),
            "--corpus",
            str(path),
        ],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert path.read_bytes() == before
    assert list(tmp_path.iterdir()) == [path]
    return process, json.loads(process.stdout)


def test_cli_leitura_sem_republicar_prova_ou_criar_arquivo(tmp_path, calibration):
    process, profile = run_cli(tmp_path, json.dumps(corpus(), ensure_ascii=False))
    assert process.returncode == 0
    assert profile["coverage"]["eligible"] == 2
    assert profile["empirical_reference_available"] is False


@pytest.mark.parametrize(
    "text",
    [
        '{"schema_version":"1","schema_version":"2"}',
        "null",
        '{"expected_questions":NaN}',
        "{",
    ],
)
def test_cli_erro_estruturado_sem_eco_de_conteudo(tmp_path, calibration, text):
    process, result = run_cli(tmp_path, text)
    assert process.returncode == 2
    assert result["status"] == "entrada_invalida"
    assert result["errors"]


def test_auditor_compara_perfil_recomputado_sem_impor_quota(calibration):
    import auditar_questoes
    from test_auditar_questoes import codes, questao

    profile = calibration.build_calibration_profile(corpus(evidence_kind="official"))
    result = auditar_questoes.audit_question_block(
        [questao(auditar_questoes)], {"q1": "C"}, profile
    )
    assert not result["errors"]
    comparison = result["metrics"]["calibration"]
    assert comparison["performed"] is True
    assert comparison["reference_sample_size"] == 2
    assert comparison["block_sample_size"] == 1
    assert comparison["format_deltas"]["direto"] == 0.5
    assert comparison["format_deltas"]["vf"] == -0.5
    assert "profile_not_validated" not in codes(result, "not_checked")
    assert "calibration_small_sample" in codes(result, "warnings")
    schema = json.loads(
        (ROOT / "modelos/pedagogia/question-block-audit.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema).validate(result)


def test_auditor_nao_trata_fixture_sintetica_como_perfil_empirico(calibration):
    import auditar_questoes
    from test_auditar_questoes import codes, questao

    result = auditar_questoes.audit_question_block(
        [questao(auditar_questoes)],
        profile=calibration.build_calibration_profile(corpus()),
    )
    assert result["metrics"]["calibration"]["performed"] is False
    assert "profile_not_empirical" in codes(result, "not_checked")


def test_auditor_rejeita_perfil_reconhecido_adulterado(calibration):
    import auditar_questoes
    from test_auditar_questoes import codes, questao

    profile = calibration.build_calibration_profile(corpus(evidence_kind="official"))
    profile["coverage"]["eligible"] = 100
    result = auditar_questoes.audit_question_block(
        [questao(auditar_questoes)], profile=profile
    )
    assert "invalid_profile" in codes(result)
    assert result["metrics"]["calibration"]["performed"] is False


def test_erro_no_bloco_impede_comparacao_com_corpus(calibration):
    import auditar_questoes
    from test_auditar_questoes import questao

    question = questao(auditar_questoes)
    question.alternatives.pop()
    result = auditar_questoes.audit_question_block(
        [question],
        profile=calibration.build_calibration_profile(corpus(evidence_kind="official")),
    )
    assert result["errors"]
    assert result["metrics"]["calibration"]["performed"] is False


@pytest.mark.parametrize("value", [2.0, True])
def test_perfil_nao_aceita_tipo_de_contagem_trocado(calibration, value):
    profile = calibration.build_calibration_profile(corpus())
    if value is True:
        profile["distributions"]["formats"]["counts"]["vf"] = value
    else:
        profile["coverage"]["eligible"] = value
    with pytest.raises(ValueError):
        calibration.validate_calibration_profile(profile)


def test_sem_chave_no_bloco_perfil_nao_concede_aprovacao_global(calibration):
    import auditar_questoes
    from test_auditar_questoes import questao

    result = auditar_questoes.audit_question_block(
        [questao(auditar_questoes)],
        profile=calibration.build_calibration_profile(corpus(evidence_kind="official")),
    )
    assert result["status"] == "checagem_parcial"
    assert result["metrics"]["calibration"]["performed"] is True


def test_novo_rotulo_de_dificuldade_divergente_permanece_pendente(calibration):
    data = corpus()
    second = review("r2")
    second["difficulty"]["label"] = "media"
    data["questions"][0]["reviews"].append(second)
    profile = calibration.build_calibration_profile(data)
    assert profile["coverage"]["eligible"] == 1
    assert profile["distributions"]["difficulty"]["counts"] == {"alta": 1}
    assert "classification_unresolved" in profile["exclusions"][0]["reasons"]
