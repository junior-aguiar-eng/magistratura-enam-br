from pathlib import Path

REFERENCE_PATH = (
    Path(__file__).resolve().parents[1] / "references" / "questoes-interativas-mcp.md"
)


def load_server_instructions() -> str:
    """Lê a orientação transmitida em initialize, a partir da referência canônica."""
    text = REFERENCE_PATH.read_text(encoding="utf-8")
    start = "<!-- mcp-instructions:start -->"
    end = "<!-- mcp-instructions:end -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError("Bloco de instruções MCP ausente, incompleto ou duplicado")
    body_start = text.index(start) + len(start)
    body_end = text.index(end)
    body = text[body_start:body_end].strip()
    if body_end < body_start or not body:
        raise ValueError("Bloco de instruções MCP vazio ou fora de ordem")
    return body
