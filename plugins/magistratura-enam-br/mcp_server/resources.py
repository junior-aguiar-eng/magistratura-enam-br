from pathlib import Path

UI_URI = "ui://estudo-juridico/questao/v2.html"
LEGACY_UI_URI = "ui://estudo-juridico/questao/v1.html"
UI_MIME_TYPE = "text/html;profile=mcp-app"


def load_question_widget() -> str:
    path = Path(__file__).resolve().parent.parent / "web" / "dist" / "index.html"
    if not path.is_file():
        raise FileNotFoundError("Widget não compilado; execute npm run build em web")
    return path.read_text(encoding="utf-8")
