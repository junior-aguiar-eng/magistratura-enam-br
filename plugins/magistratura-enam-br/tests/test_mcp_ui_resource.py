import copy
import json
import tomllib
from pathlib import Path

import pytest
from mcp.client import Client
from test_mcp_question_sessions import sessao

from mcp_server.config import LibraryConfig
from mcp_server.server import build_server

UI_URI = "ui://estudo-juridico/questao/v2.html"
LEGACY_UI_URI = "ui://estudo-juridico/questao/v1.html"


@pytest.fixture
def server(tmp_path):
    root = tmp_path / "biblioteca"
    root.mkdir()
    (root / ".estudo-juridico").mkdir()
    return build_server(
        LibraryConfig(
            library_root=root.resolve(),
            excluded_directories=(".git", ".estudo-juridico", "node_modules"),
            max_file_bytes=2_000_000,
            max_result_chunks=12,
        )
    )


@pytest.mark.anyio
async def test_apenas_renderizador_declara_recurso_ui(server):
    async with Client(server) as client:
        tools = await client.list_tools()

    by_name = {tool.name: tool for tool in tools.tools}
    render_meta = by_name["renderizar_questao"].meta
    assert render_meta["ui"] == {
        "resourceUri": UI_URI,
        "visibility": ["model", "app"],
    }
    assert render_meta["openai/outputTemplate"] == UI_URI
    assert render_meta["openai/widgetAccessible"] is True
    assert render_meta["openai/toolInvocation/invoking"] == "Abrindo questão…"
    assert render_meta["openai/toolInvocation/invoked"] == "Questão pronta"
    for name, tool in by_name.items():
        if name != "renderizar_questao":
            assert tool.meta is None or "ui" not in tool.meta


@pytest.mark.anyio
async def test_servidor_publica_versao_real_do_pacote(server):
    async with Client(server) as client:
        version = client.server_info.version

    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    package_version = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
    assert version == package_version


@pytest.mark.anyio
async def test_recurso_ui_e_autocontido(server):
    async with Client(server) as client:
        result = await client.read_resource(UI_URI)

    resource = result.contents[0]
    assert resource.mime_type == "text/html;profile=mcp-app"
    assert resource.meta["ui"]["prefersBorder"] is True
    assert resource.meta["openai/widgetPrefersBorder"] is True
    assert resource.meta["openai/widgetDescription"] == (
        "Questão jurídica objetiva com correção após a tentativa."
    )
    assert resource.meta["openai/widgetCSP"] == {
        "connect_domains": [],
        "resource_domains": [],
    }
    assert '<div id="root"></div>' in resource.text
    assert "<script" in resource.text
    assert "<style" in resource.text


@pytest.mark.anyio
async def test_recurso_ui_anterior_permanece_disponivel_durante_atualizacao(server):
    async with Client(server) as client:
        current = await client.read_resource(UI_URI)
        legacy = await client.read_resource(LEGACY_UI_URI)

    assert legacy.contents[0].mime_type == current.contents[0].mime_type
    assert legacy.contents[0].text == current.contents[0].text


@pytest.mark.anyio
async def test_renderizador_entrega_somente_projecao_publica(server):
    question = copy.deepcopy(sessao())
    for field in ("schema_version", "projection", "session_id", "state", "created_at"):
        question.pop(field)

    async with Client(server) as client:
        created = await client.call_tool("criar_sessao_questao", {"questao": question})
        rendered = await client.call_tool(
            "renderizar_questao",
            {"session_id": created.structured_content["session_id"]},
        )

    serialized = json.dumps(rendered.structured_content, ensure_ascii=False)
    assert rendered.structured_content["projection"] == "public"
    assert "correct_option" not in serialized
    assert "correct_rationale" not in serialized
    assert "distractor_analysis" not in serialized
