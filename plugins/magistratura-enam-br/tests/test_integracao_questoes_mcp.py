import copy

import pytest
from mcp.client import Client

from mcp_server.config import LibraryConfig
from mcp_server.server import build_server
from test_mcp_question_sessions import sessao


def test_referencia_mcp_preserva_substancia_na_skill(texto):
    skill = texto("skills/estudar-direito-magistratura/SKILL.md")
    contract = texto("references/contrato-pedagogico.md")
    sources = texto("references/politica-fontes-juridicas.md")
    integration = texto("references/questoes-interativas-mcp.md")

    assert "references/questoes-interativas-mcp.md" in skill
    assert "cinco alternativas" in integration
    assert "gabarito único" in integration
    assert "análise integral dos quatro distratores" in integration
    assert "Planalto → STF/STJ → acervo local → fonte jurídica subsidiária" in sources
    assert "source_status: caution" in integration
    assert "aviso explícito de cuidado" in integration
    assert "fallback textual" in integration
    assert "não antecipa o gabarito" in integration
    assert "questão é gerada pelo modelo" in contract
    assert "MCP não define a substância jurídica" in contract


@pytest.mark.anyio
async def test_fluxo_mcp_completo_preserva_gabarito_ate_tentativa(tmp_path):
    root = tmp_path / "biblioteca"
    root.mkdir()
    (root / ".estudo-juridico").mkdir()
    (root / "cpc.md").write_text("# CPC\n\nProva pericial e contraditório.", encoding="utf-8")
    server = build_server(
        LibraryConfig(
            library_root=root.resolve(),
            excluded_directories=(".git", ".estudo-juridico", "node_modules"),
            max_file_bytes=2_000_000,
            max_result_chunks=12,
        )
    )
    question = copy.deepcopy(sessao())
    for field in ("schema_version", "projection", "session_id", "state", "created_at"):
        question.pop(field)

    async with Client(server) as client:
        await client.call_tool("indexar_acervo", {"confirmar_gravacao_local": True})
        search = await client.call_tool("buscar_acervo", {"consulta": "prova pericial"})
        created = await client.call_tool("criar_sessao_questao", {"questao": question})
        rendered = await client.call_tool(
            "renderizar_questao", {"session_id": created.structured_content["session_id"]}
        )
        answered = await client.call_tool(
            "responder_questao",
            {"session_id": created.structured_content["session_id"], "alternativa": "B"},
        )

    assert search.structured_content["results"]
    assert "correct_option" not in created.structured_content
    assert "correct_option" not in rendered.structured_content
    assert answered.structured_content["correct_option"] == "C"
    assert len(answered.structured_content["correction"]["distractor_analysis"]) == 4
