import copy
import json

import pytest
from mcp.client import Client
from test_mcp_question_sessions import sessao

from mcp_server.config import LibraryConfig
from mcp_server.server import build_server


@pytest.fixture
def services(tmp_path):
    raiz = tmp_path / "biblioteca"
    raiz.mkdir()
    (raiz / "civil.md").write_text(
        "# Obrigações\n\nO inadimplemento pode gerar perdas e danos.", encoding="utf-8"
    )
    (raiz / ".estudo-juridico").mkdir()
    config = LibraryConfig(
        library_root=raiz.resolve(),
        excluded_directories=(".git", ".estudo-juridico", "node_modules"),
        max_file_bytes=2_000_000,
        max_result_chunks=12,
    )
    return build_server(config), raiz


@pytest.mark.anyio
async def test_cliente_mcp_real_descobre_as_ferramentas_de_dados(services):
    server, _ = services

    async with Client(server) as client:
        result = await client.list_tools()

    assert {tool.name for tool in result.tools} >= {
        "indexar_acervo",
        "buscar_acervo",
        "diagnosticar_acervo",
        "criar_sessao_questao",
        "responder_questao",
        "consultar_historico_questoes",
    }
    assert all(
        tool.meta is None or "ui" not in tool.meta
        for tool in result.tools
        if tool.name != "renderizar_questao"
    )
    diagnostico = next(tool for tool in result.tools if tool.name == "diagnosticar_acervo")
    assert diagnostico.annotations.read_only_hint is True


@pytest.mark.anyio
async def test_indexacao_e_busca_funcionam_por_cliente_mcp(services):
    server, raiz = services

    async with Client(server) as client:
        indexado = await client.call_tool(
            "indexar_acervo", {"confirmar_gravacao_local": True}
        )
        busca = await client.call_tool(
            "buscar_acervo", {"consulta": "inadimplemento perdas", "limite": 5}
        )

    assert indexado.structured_content["document_count"] == 1
    assert (raiz / ".estudo-juridico" / "index.json").is_file()
    assert busca.structured_content["results"][0]["relative_path"] == "civil.md"


@pytest.mark.anyio
async def test_criacao_mcp_gera_id_e_nao_devolve_gabarito(services):
    server, _ = services
    question = copy.deepcopy(sessao())
    for field in ("schema_version", "projection", "session_id", "state", "created_at"):
        question.pop(field)

    async with Client(server) as client:
        created = await client.call_tool("criar_sessao_questao", {"questao": question})

    payload = created.structured_content
    serialized = json.dumps(payload, ensure_ascii=False)
    assert payload["session_id"].startswith("qsn_")
    assert payload["projection"] == "public"
    assert "correct_option" not in serialized
    assert "correct_rationale" not in serialized
    assert "distractor_analysis" not in serialized


@pytest.mark.anyio
async def test_resposta_e_historico_funcionam_por_cliente_mcp(services):
    server, _ = services
    question = copy.deepcopy(sessao())
    for field in ("schema_version", "projection", "session_id", "state", "created_at"):
        question.pop(field)

    async with Client(server) as client:
        created = await client.call_tool("criar_sessao_questao", {"questao": question})
        session_id = created.structured_content["session_id"]
        answered = await client.call_tool(
            "responder_questao", {"session_id": session_id, "alternativa": "B"}
        )
        history = await client.call_tool(
            "consultar_historico_questoes", {"limite": 10, "cursor": 0}
        )

    assert answered.structured_content["state"] == "answered"
    assert answered.structured_content["correct_option"] == "C"
    assert history.structured_content["items"][0]["session_id"] == session_id
    assert history.structured_content["items"][0]["result"] == "incorrect"


@pytest.mark.anyio
async def test_indexacao_exige_confirmacao_explicita(services):
    server, raiz = services

    async with Client(server) as client:
        result = await client.call_tool(
            "indexar_acervo", {"confirmar_gravacao_local": False}
        )

    assert result.is_error
    assert not (raiz / ".estudo-juridico" / "index.json").exists()


@pytest.mark.anyio
async def test_diagnostico_sem_indice_informa_caminhos_sem_escrever(services):
    server, raiz = services
    estado = raiz / ".estudo-juridico"
    antes = sorted(item.name for item in estado.iterdir())

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    payload = result.structured_content
    assert payload == {
        "schema_version": "1.0.0",
        "library_root": str(raiz.resolve()),
        "state_dir": str(estado.resolve()),
        "index_path": str((estado / "index.json").resolve()),
        "index_status": "missing",
        "document_count": None,
        "generated_at": None,
    }
    assert sorted(item.name for item in estado.iterdir()) == antes


@pytest.mark.anyio
async def test_diagnostico_indice_valido_informa_metadados_sem_conteudo(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    async with Client(server) as client:
        await client.call_tool("indexar_acervo", {"confirmar_gravacao_local": True})
        antes = indice.read_bytes()
        result = await client.call_tool("diagnosticar_acervo", {})

    payload = result.structured_content
    assert payload["index_status"] == "available"
    assert payload["document_count"] == 1
    assert payload["generated_at"] == json.loads(antes)["generated_at"]
    assert "civil.md" not in json.dumps(payload)
    assert "inadimplemento" not in json.dumps(payload)
    assert indice.read_bytes() == antes


@pytest.mark.anyio
async def test_diagnostico_indice_invalido_preserva_arquivo(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    indice.write_text("{invalido", encoding="utf-8")
    antes = indice.read_bytes()

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    payload = result.structured_content
    assert payload["index_status"] == "invalid"
    assert payload["document_count"] is None
    assert payload["generated_at"] is None
    assert indice.read_bytes() == antes


@pytest.mark.anyio
async def test_diagnostico_manifesto_sem_documentos_validos_nao_conta_caracteres(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    indice.write_text('{"schema_version":"1.0.0","generated_at":"2026-09-24T12:00:00Z","documents":"texto"}', encoding="utf-8")

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "invalid"


@pytest.mark.anyio
async def test_diagnostico_rejeita_documento_incompleto(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    indice.write_text('{"schema_version":"1.0.0","generated_at":"2026-09-24T12:00:00Z","documents":[{}]}', encoding="utf-8")

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "invalid"


@pytest.mark.anyio
async def test_diagnostico_rejeita_data_sem_fuso(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    indice.write_text('{"schema_version":"1.0.0","generated_at":"2026-09-24","documents":[]}', encoding="utf-8")

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "invalid"


@pytest.mark.anyio
async def test_diagnostico_diretorio_no_caminho_do_indice_e_invalido(services):
    server, raiz = services
    indice = raiz / ".estudo-juridico" / "index.json"
    indice.mkdir()

    async with Client(server) as client:
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "invalid"
    assert indice.is_dir()


@pytest.mark.anyio
async def test_diagnostico_aceita_indice_criado_com_cabecalho_longo_e_extensao_maiuscula(services):
    server, raiz = services
    (raiz / "LONGO.MD").write_text("# " + "X" * 501 + "\n\nConteúdo.", encoding="utf-8")

    async with Client(server) as client:
        await client.call_tool("indexar_acervo", {"confirmar_gravacao_local": True})
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "available"
    assert result.structured_content["document_count"] == 2


@pytest.mark.anyio
async def test_diagnostico_aceita_indice_criado_com_h1_em_branco(services):
    server, raiz = services
    (raiz / "branco.md").write_text("#   \n\nConteúdo.", encoding="utf-8")

    async with Client(server) as client:
        await client.call_tool("indexar_acervo", {"confirmar_gravacao_local": True})
        result = await client.call_tool("diagnosticar_acervo", {})

    assert result.structured_content["index_status"] == "available"
    assert result.structured_content["document_count"] == 2
