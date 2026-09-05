import json
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from mcp import StdioServerParameters
from mcp.client import Client

from mcp_server.server import build_parser


def test_cli_oferece_stdio_e_streamable_http_com_limites_locais(tmp_path):
    parser = build_parser()
    config = tmp_path / "config.json"

    stdio = parser.parse_args(["--config", str(config), "--transport", "stdio"])
    http = parser.parse_args(
        [
            "--config",
            str(config),
            "--transport",
            "streamable-http",
            "--host",
            "127.0.0.1",
            "--port",
            "8765",
        ]
    )

    assert stdio.config == Path(config)
    assert stdio.transport == "stdio"
    assert http.transport == "streamable-http"
    assert http.host == "127.0.0.1"
    assert http.port == 8765


def test_cli_rejeita_transporte_e_porta_invalidos(tmp_path):
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["--config", str(tmp_path / "config.json"), "--transport", "sse"])
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--config",
                str(tmp_path / "config.json"),
                "--transport",
                "streamable-http",
                "--port",
                "70000",
            ]
        )


@pytest.mark.anyio
async def test_config_bundled_inicia_servidor_stdio_real(tmp_path):
    plugin_root = Path(__file__).resolve().parents[1]
    library = tmp_path / "biblioteca"
    library.mkdir()
    (library / ".estudo-juridico").mkdir()
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "library-config.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "library_root": str(library),
                "write_consent": True,
                "excluded_directories": [".git", ".estudo-juridico", "node_modules"],
                "limits": {"max_file_bytes": 2_000_000, "max_result_chunks": 12},
            }
        ),
        encoding="utf-8",
    )
    bundled = json.loads((plugin_root / ".mcp.json").read_text(encoding="utf-8"))
    definition = bundled["estudo-juridico-avancado"]
    args = [
        arg.replace("${PLUGIN_ROOT}", str(plugin_root)).replace("${PLUGIN_DATA}", str(data))
        for arg in definition["args"]
    ]

    async with Client(StdioServerParameters(command=definition["command"], args=args)) as client:
        tools = await client.list_tools()

    by_name = {tool.name: tool for tool in tools.tools}
    assert "renderizar_questao" in by_name
    creation = by_name["criar_sessao_questao"]
    creation_schema = json.dumps(creation.input_schema)
    assert all(field in creation_schema for field in ("subject", "alternatives", "correct_option"))
    assert creation.annotations.destructive_hint is False
    assert creation.annotations.open_world_hint is False
    assert by_name["buscar_acervo"].annotations.read_only_hint is True


@pytest.mark.anyio
async def test_transporte_http_local_aceita_cliente_mcp_real(tmp_path):
    library = tmp_path / "biblioteca-http"
    library.mkdir()
    (library / ".estudo-juridico").mkdir()
    config = tmp_path / "config-http.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "library_root": str(library),
                "write_consent": True,
                "excluded_directories": [".git", ".estudo-juridico", "node_modules"],
                "limits": {"max_file_bytes": 2_000_000, "max_result_chunks": 12},
            }
        ),
        encoding="utf-8",
    )
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "mcp_server.server",
            "--config",
            str(config),
            "--transport",
            "streamable-http",
            "--port",
            str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            with socket.socket() as probe:
                if probe.connect_ex(("127.0.0.1", port)) == 0:
                    break
            time.sleep(0.05)
        async with Client(f"http://127.0.0.1:{port}/mcp") as client:
            tools = await client.list_tools()
        assert "criar_sessao_questao" in {tool.name for tool in tools.tools}
    finally:
        process.terminate()
        process.wait(timeout=5)
