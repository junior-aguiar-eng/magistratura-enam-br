from pathlib import Path

import pytest

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
