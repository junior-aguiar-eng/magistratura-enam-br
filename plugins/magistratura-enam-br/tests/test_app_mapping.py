import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mapeamento_privado_usa_id_tecnico_sem_segredos():
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    mapping = json.loads((ROOT / ".app.json").read_text(encoding="utf-8"))

    assert manifest["apps"] == "./.app.json"
    serialized = json.dumps(mapping)
    ids = re.findall(r"plugin_asdk_app_[0-9a-z]+", serialized)
    assert len(ids) == 1
    assert not any(term in serialized.casefold() for term in ("api_key", "secret", "password", "tunnel_id"))
