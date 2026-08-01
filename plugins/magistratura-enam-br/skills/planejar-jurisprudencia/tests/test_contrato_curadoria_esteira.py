import json
import subprocess
import sys
from pathlib import Path

import preparar_itens_esteira as preparador

ROOT = Path(__file__).resolve().parents[3]
ATUALIZADOR_CURADORIA = ROOT / "skills" / "curar-informativos-stf-stj" / "scripts" / "atualizar_planilha_precedentes.py"


def test_planilha_da_curadoria_e_lida_pela_esteira_com_metadados(tmp_path):
    entrada = tmp_path / "precedentes.json"
    planilha = tmp_path / "precedentes.xlsx"
    entrada.write_text(json.dumps([{
        "processo": "RE 123456",
        "tema": "Responsabilidade civil do Estado",
        "tribunal": "STF",
        "orgao_julgador": "Plenário",
        "disciplina": "Constitucional",
        "estado_jurisprudencial": "confirmado",
        "grau_confianca": "alto",
        "data_julgamento": "2025-01-10",
        "data_informativo": "2025-02-01",
        "tese_resumida": "Tese de teste",
        "fontes_essenciais": ["acórdão oficial", "informativo"],
        "nota_estado": "",
    }], ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(ATUALIZADOR_CURADORIA), str(entrada), str(planilha), "--data-inclusao", "2026-01-01"],
        check=True, capture_output=True, text=True,
    )
    registros = preparador.ler_precedentes(planilha)
    itens, excluidos = preparador.converter(registros, set(), set(), {}, False)

    assert excluidos == 0
    assert itens == [{
        "id": "STF|RE123456|PLENÁRIO|2025-01-10|TESE DE TESTE", "tema": "Responsabilidade civil do Estado", "tribunal": "STF",
        "disciplina": "Constitucional", "estado_jurisprudencial": "confirmado",
        "grau_confianca": "alto", "fontes_essenciais": "acórdão oficial\ninformativo",
        "prioridade": "padrao", "motivo_prioridade": "prioridade padrão", "origem_erro": "nao",
    }]
