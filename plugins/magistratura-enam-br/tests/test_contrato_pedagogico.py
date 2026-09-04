import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRATO = ROOT / "references" / "contrato-pedagogico.md"

TAXONOMIA_V1 = {
    "modalidades": [
        "explicacao",
        "recuperacao",
        "consolidacao",
        "vespera",
        "questao_objetiva",
        "discursiva_curta",
        "prova_oral",
        "leitura_julgado",
        "revisao_julgado",
    ],
    "resultados": ["nao_avaliado", "correto", "parcial", "incorreto", "questao_invalida"],
    "tipos_de_erro": [
        "conceito",
        "pressuposto",
        "regra",
        "excecao",
        "competencia",
        "legitimidade",
        "prazo",
        "efeito",
        "suporte_fatico",
        "distincao",
        "atualizacao_normativa",
        "atualizacao_jurisprudencial",
        "fundamentacao",
        "expressao_oral",
        "estrutura_discursiva",
    ],
    "evidencias_de_dominio": [
        "evocacao_regra",
        "discriminacao_institutos",
        "aplicacao_fatos_novos",
        "fundamentacao_normativa_jurisprudencial",
        "expressao_objetiva_discursiva_oral",
        "retencao_revisao_posterior",
    ],
}


def carregar_taxonomia() -> dict:
    texto = CONTRATO.read_text(encoding="utf-8")
    bloco = re.search(r"<!-- taxonomia-v1 -->\s*```json\s*(.*?)\s*```", texto, re.DOTALL)
    assert bloco is not None, "Contrato sem bloco JSON da taxonomia v1."
    return json.loads(bloco.group(1))


def test_contrato_publica_taxonomia_v1_exata_sem_duplicatas():
    taxonomia = carregar_taxonomia()

    assert taxonomia == TAXONOMIA_V1
    assert all(len(valores) == len(set(valores)) for valores in taxonomia.values())


def test_contrato_proibe_inferencia_de_erro_sem_tentativa_observavel():
    texto = CONTRATO.read_text(encoding="utf-8").casefold()

    assert "tentativa observável" in texto
    assert "não autoriza inferir erro" in texto
    assert "comparar-materiais-enam" in texto

