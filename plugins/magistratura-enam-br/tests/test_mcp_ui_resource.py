import copy
import json
import tomllib
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError
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
    assert by_name["responder_questao"].meta["openai/widgetAccessible"] is True
    for name, tool in by_name.items():
        if name != "renderizar_questao":
            assert tool.meta is None or "resourceUri" not in tool.meta.get("ui", {})


@pytest.mark.anyio
async def test_servidor_anuncia_instrucoes_canonicas(server):
    async with Client(server) as client:
        instructions = client.instructions
    assert instructions
    from mcp_server.instructions import load_server_instructions

    assert instructions == load_server_instructions()
    for rule in (
        "cinco alternativas",
        "gabarito único",
        "quatro distratores",
        "correção integral",
        "invalidar_questao",
        "fallback textual",
        "consentimento",
        "STF",
        "anexos",
    ):
        assert rule in instructions


@pytest.mark.anyio
async def test_visibilidade_resposta_modelo_e_app(server):
    async with Client(server) as client:
        tools = (await client.list_tools()).tools
    by_name = {tool.name: tool for tool in tools}
    for name in ("renderizar_questao", "responder_questao", "obter_questao"):
        assert by_name[name].meta["ui"]["visibility"] == ["model", "app"]
    assert "resourceUri" not in by_name["responder_questao"].meta["ui"]
    assert by_name["responder_questao"].annotations.read_only_hint is False
    assert by_name["responder_questao"].annotations.idempotent_hint is True
    assert by_name["renderizar_questao"].annotations.read_only_hint is True
    for name, tool in by_name.items():
        assert tool.annotations.open_world_hint is False
        assert tool.annotations.destructive_hint is False
        if name not in ("renderizar_questao", "responder_questao", "obter_questao"):
            assert tool.meta["ui"]["visibility"] == ["model"]


@pytest.mark.anyio
async def test_schema_saida_publica_nao_exige_gabarito(server):
    question = copy.deepcopy(sessao())
    for field in ("schema_version", "projection", "session_id", "state", "created_at"):
        question.pop(field)
    async with Client(server) as client:
        tools = {tool.name: tool for tool in (await client.list_tools()).tools}
        schemas = {name: tool.output_schema for name, tool in tools.items()}
        for schema in schemas.values():
            assert schema.get("required")
            Draft202012Validator.check_schema(schema)
        results = []
        results.append(
            ("diagnosticar_acervo", await client.call_tool("diagnosticar_acervo", {}))
        )
        # Reading the diagnostic does not authorize writing an index.
        denied = await client.call_tool("indexar_acervo", {})
        assert denied.is_error
        results.append(
            (
                "indexar_acervo",
                await client.call_tool(
                    "indexar_acervo", {"confirmar_gravacao_local": True}
                ),
            )
        )
        results.append(
            (
                "buscar_acervo",
                await client.call_tool("buscar_acervo", {"consulta": "civil"}),
            )
        )
        created = await client.call_tool("criar_sessao_questao", {"questao": question})
        results.append(("criar_sessao_questao", created))
        public = created.structured_content
        session_id = public["session_id"]
        assert public["projection"] == "public"
        assert "correct_option" not in json.dumps(public)
        assert "correction" not in public
        private = {
            **public,
            "projection": "private",
            "correct_option": question["correct_option"],
            "correction": question["correction"],
        }
        for name in ("criar_sessao_questao", "renderizar_questao"):
            with pytest.raises(ValidationError):
                Draft202012Validator(schemas[name]).validate(private)
            with pytest.raises(ValidationError):
                Draft202012Validator(schemas[name]).validate(
                    {**public, "correct_option": question["correct_option"]}
                )
        results.append(
            (
                "renderizar_questao",
                await client.call_tool(
                    "renderizar_questao", {"session_id": session_id}
                ),
            )
        )
        answered = await client.call_tool(
            "responder_questao",
            {"session_id": session_id, "alternativa": question["correct_option"]},
        )
        results.append(("responder_questao", answered))
        assert answered.structured_content["projection"] == "corrected"
        assert answered.structured_content["result"] == "correct"
        assert answered.structured_content["correction"] == question["correction"]
        results.append(
            (
                "renderizar_questao",
                await client.call_tool(
                    "renderizar_questao", {"session_id": session_id}
                ),
            )
        )
        results.append(
            (
                "consultar_historico_questoes",
                await client.call_tool("consultar_historico_questoes", {}),
            )
        )
        invalidated = await client.call_tool(
            "invalidar_questao",
            {"session_id": session_id, "motivo": "Fixture inválida para estudo real."},
        )
        results.append(("invalidar_questao", invalidated))
        assert invalidated.structured_content["state"] == "invalidated"
        assert "correct_option" not in invalidated.structured_content
    for name, result in results:
        assert not result.is_error, (name, result.content)
        Draft202012Validator(schemas[name]).validate(result.structured_content)


@pytest.mark.anyio
async def test_servidor_publica_versao_real_do_pacote(server):
    async with Client(server) as client:
        version = client.server_info.version

    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    package_version = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"][
        "version"
    ]
    assert version == package_version


@pytest.mark.anyio
async def test_recurso_ui_e_autocontido(server):
    async with Client(server) as client:
        result = await client.read_resource(UI_URI)

    resource = result.contents[0]
    assert resource.mime_type == "text/html;profile=mcp-app"
    assert resource.meta["openai/ui"]["availableDisplayModes"] == ["inline", "fullscreen"]
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

    assert legacy.contents[0].meta["openai/ui"]["availableDisplayModes"] == ["inline", "fullscreen"]
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
