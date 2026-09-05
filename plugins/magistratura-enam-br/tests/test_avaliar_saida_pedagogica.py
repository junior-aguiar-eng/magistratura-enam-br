import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "avaliar_saida_pedagogica.py"


def carregar_avaliador():
    assert SCRIPT.is_file(), "avaliador pedagógico ausente"
    spec = importlib.util.spec_from_file_location("avaliar_saida_pedagogica", SCRIPT)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def caso_questao():
    return {
        "id": "estudo-questao",
        "assertions": [
            {
                "id": "cinco-alternativas",
                "description": "Há exatamente cinco alternativas.",
                "kind": "automatic",
                "check": "option_count",
                "expected": 5,
            },
            {
                "id": "sem-gabarito",
                "description": "Não antecipa a resposta.",
                "kind": "automatic",
                "check": "forbidden_terms",
                "values": ["gabarito", "resposta correta", "alternativa correta"],
            },
            {
                "id": "encerra-em-e",
                "description": "Encerra após a alternativa E.",
                "kind": "automatic",
                "check": "ends_after_option_e",
            },
            {
                "id": "unicidade-material",
                "description": "Há uma única solução juridicamente defensável.",
                "kind": "human",
            },
        ],
    }


def test_avaliador_aprova_estrutura_da_tentativa_sem_autoavaliar_direito():
    avaliador = carregar_avaliador()
    texto = "Enunciado\nA. Solução um\nB. Solução dois\nC. Solução três\nD. Solução quatro\nE. Solução cinco"

    resultado = avaliador.avaliar_saida(caso_questao(), texto)

    assert resultado["status"] == "revisao_humana_pendente"
    assert all(item["passed"] for item in resultado["assertions"])
    assert resultado["human_review_required"] == ["unicidade-material"]


def test_avaliador_reprova_gabarito_antecipado_e_texto_apos_alternativa_e():
    avaliador = carregar_avaliador()
    texto = (
        "Enunciado\nA. Um\nB. Dois\nC. Três\nD. Quatro\nE. Cinco\n"
        "Gabarito: alternativa correta E."
    )

    resultado = avaliador.avaliar_saida(caso_questao(), texto)

    assert resultado["status"] == "reprovado"
    falhas = {item["id"] for item in resultado["assertions"] if not item["passed"]}
    assert falhas == {"sem-gabarito", "encerra-em-e"}


def test_avaliador_confere_ordem_do_comentario_jurisprudencial():
    avaliador = carregar_avaliador()
    caso = {
        "id": "curadoria-comentario",
        "assertions": [{
            "id": "ordem-comentario",
            "description": "Blocos aparecem na ordem editorial.",
            "kind": "automatic",
            "check": "ordered_markers",
            "values": [
                "Situação precedental",
                "Tese:",
                "Controvérsia e contexto",
                "Base normativa e ratio decidendi",
                "Aplicação e limites",
                "Relevância para a Magistratura",
            ],
        }],
    }
    texto = "\n".join(caso["assertions"][0]["values"])

    resultado = avaliador.avaliar_saida(caso, texto)

    assert resultado["status"] == "aprovado_estruturalmente"
    assert resultado["human_review_required"] == []


def test_avaliador_nao_aprova_automaticamente_afirmacao_semantica():
    avaliador = carregar_avaliador()
    caso = {
        "id": "dogmatica-fontes",
        "assertions": [],
        "semantic_claims": [{
            "id": "funcao-das-fontes",
            "description": "As fontes desempenham função dogmática.",
            "evidence_required": "Vínculo entre fonte e proposição.",
        }],
    }

    resultado = avaliador.avaliar_saida(caso, "Texto com artigo e precedente.")

    assert resultado["status"] == "revisao_humana_pendente"
    assert resultado["human_review_required"] == ["funcao-das-fontes"]
