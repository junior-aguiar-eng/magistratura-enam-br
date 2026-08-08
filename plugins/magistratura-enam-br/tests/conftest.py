import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


@pytest.fixture
def texto():
    def ler(relativo: str) -> str:
        return (ROOT / relativo).read_text(encoding="utf-8")

    return ler
