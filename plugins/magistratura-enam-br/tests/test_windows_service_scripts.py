from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install_local_service.ps1"
UNINSTALL = ROOT / "scripts" / "uninstall_local_service.ps1"


def test_scripts_exigem_confirmacao_explicita() -> None:
    for script in (INSTALL, UNINSTALL):
        text = script.read_text(encoding="utf-8")
        assert "[switch]$Confirm" in text
        assert "if (-not $Confirm)" in text


def test_instalacao_e_escopo_do_usuario_sao_seguros() -> None:
    text = INSTALL.read_text(encoding="utf-8")
    assert "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" in text
    assert "Start-Process" in text
    assert "-WorkingDirectory" in text
    assert "CONTROL_PLANE_API_KEY" in text
    assert "ConvertTo-Json" in text
    assert "-WindowStyle Hidden" in text
    assert "$quotedProfile" in text
    assert "@('run', '--config', $quotedProfile)" in text


def test_desinstalacao_e_simetrica_e_preserva_dados() -> None:
    text = UNINSTALL.read_text(encoding="utf-8")
    assert "Remove-ItemProperty" in text
    assert "runner.ps1" in text
    assert "library-config.json" not in text
    assert "questoes.jsonl" not in text
    assert "tentativas.jsonl" not in text
    assert "-Recurse" not in text
