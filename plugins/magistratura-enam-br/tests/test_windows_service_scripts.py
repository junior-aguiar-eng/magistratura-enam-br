import json
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install_local_service.ps1"
UNINSTALL = ROOT / "scripts" / "uninstall_local_service.ps1"
RUNNER = ROOT / "scripts" / "local_service_runner.ps1"


def test_scripts_exigem_confirmacao_explicita() -> None:
    for script in (INSTALL, UNINSTALL):
        text = script.read_text(encoding="utf-8")
        assert "[switch]$Confirm" in text
        assert "if (-not $Confirm)" in text


def test_instalacao_e_escopo_do_usuario_sao_seguros() -> None:
    text = INSTALL.read_text(encoding="utf-8")
    assert ".runtime\\startup" in text
    assert "Estudo Jurídico Avançado\\startup" not in text
    assert "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" in text
    assert "-WorkingDirectory $runtimeDirectory" not in text
    assert "CONTROL_PLANE_API_KEY" in text
    assert "ConvertTo-Json" in text
    assert "-WindowStyle Hidden" in text
    assert "local_service_runner.ps1" in text
    assert '-File `"$sourceRunnerPath`"' in text
    assert '-TunnelClientPath `"$tunnelClient`"' in text
    assert '-RuntimeDirectory `"$runtimeDirectory`"' in text
    assert "Copy-Item -LiteralPath $tunnelProfile" in text
    assert "$runtimeProfilePath" in text
    assert "Copy-Item -LiteralPath $sourceRunnerPath" not in text
    assert "Register-ScheduledTask" in text
    assert "Start-ScheduledTask" in text
    assert "RestartCount 999" in text
    assert "MultipleInstances IgnoreNew" in text
    assert "Set-ItemProperty" not in text
    assert "& $runnerPath" not in text


def test_runner_e_idempotente_e_registra_falhas_operacionais() -> None:
    text = RUNNER.read_text(encoding="utf-8")

    assert "[string]$TunnelClientPath" in text
    assert "[string]$RuntimeDirectory" in text
    assert "New-Item -ItemType Directory" in text
    assert "Get-CimInstance Win32_Process" in text
    assert "ExecutablePath" in text
    assert "-ieq $clientPath" in text
    assert "RedirectStandardOutput" in text
    assert "RedirectStandardError" in text
    assert "tunnel-client.stdout.log" in text
    assert "tunnel-client.stderr.log" in text
    assert "$quotedProfile" in text
    assert "@('run', '--config', $quotedProfile)" in text


def test_supervisor_reinicia_tunnel_que_encerra_inesperadamente(tmp_path: Path) -> None:
    if not RUNNER.is_file():
        pytest.fail("runner supervisor ainda não foi implementado")

    powershell = shutil.which("powershell.exe")
    disposable_executable = shutil.which("where.exe")
    assert powershell is not None
    assert disposable_executable is not None

    runtime = tmp_path / "runtime"
    runtime.mkdir()
    runner = runtime / "runner.ps1"
    shutil.copy2(RUNNER, runner)
    tunnel = runtime / "tunnel-client.exe"
    shutil.copy2(disposable_executable, tunnel)
    profile = runtime / "profile.yaml"
    profile.write_text("test: true\n", encoding="utf-8")
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (runtime / "startup.json").write_text(
        json.dumps(
            {
                "tunnel_client": str(tunnel),
                "tunnel_profile": str(profile),
                "working_directory": str(workspace),
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            powershell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(runner),
            "-RestartDelaySeconds",
            "0",
            "-MaxStarts",
            "2",
            "-MutexName",
            f"Local\\EstudoJuridicoTeste-{uuid.uuid4()}",
        ],
        cwd=runtime,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    supervisor_log = (runtime / "supervisor.log").read_text(encoding="utf-8")
    assert supervisor_log.count("started tunnel pid=") == 2


def test_desinstalacao_e_simetrica_e_preserva_dados() -> None:
    text = UNINSTALL.read_text(encoding="utf-8")
    assert ".runtime\\startup" in text
    assert "tunnel-profile.yaml" in text
    assert "Remove-ItemProperty" in text
    assert "runner.ps1" in text
    assert "library-config.json" not in text
    assert "questoes.jsonl" not in text
    assert "tentativas.jsonl" not in text
    assert "-Recurse" not in text
    assert "tunnel-client.stdout.log" in text
    assert "tunnel-client.stderr.log" in text
    assert "expectedClientPath" in text
    assert "$process.Path" in text
    assert "supervisor.pid" in text
    assert "supervisor.log" in text
    assert "expectedRunnerPath" in text
    assert "Join-Path $PSScriptRoot 'local_service_runner.ps1'" in text
    assert "Stop-ScheduledTask" in text
    assert "Unregister-ScheduledTask" in text
