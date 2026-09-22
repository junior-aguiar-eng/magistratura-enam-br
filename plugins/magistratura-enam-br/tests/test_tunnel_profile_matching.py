import shutil
import subprocess
import uuid
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "scripts" / "local_service_runner.ps1"


def test_supervisor_ignora_tunnel_com_outro_perfil(tmp_path: Path) -> None:
    powershell = shutil.which("powershell.exe")
    assert powershell is not None
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    runner = runtime / "runner.ps1"
    shutil.copy2(RUNNER, runner)
    tunnel = runtime / "tunnel-client.exe"
    shutil.copy2(powershell, tunnel)
    expected_profile = runtime / "expected.yaml"
    expected_profile.write_text("test: true\n", encoding="utf-8")
    other_profile = runtime / "other.yaml"
    other_profile.write_text("test: false\n", encoding="utf-8")
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    other_tunnel = subprocess.Popen(
        [str(tunnel), "-NoProfile", "-Command", f"Start-Sleep -Seconds 120; # --config {other_profile} ignored"],
        cwd=runtime,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        assert other_tunnel.poll() is None
        result = subprocess.run(
            [
                powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner),
                "-TunnelClientPath", str(tunnel), "-TunnelProfilePath", str(expected_profile),
                "-WorkingDirectory", str(workspace), "-RuntimeDirectory", str(runtime),
                "-RestartDelaySeconds", "0", "-MaxStarts", "1",
                "-MutexName", f"Local\\EstudoJuridicoTeste-{uuid.uuid4()}",
            ],
            cwd=runtime,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        log = (runtime / "supervisor.log").read_text(encoding="utf-8")
        assert "started tunnel pid=" in log
        assert f"attached tunnel pid={other_tunnel.pid}" not in log
    finally:
        other_tunnel.terminate()
        try:
            other_tunnel.wait(timeout=5)
        except subprocess.TimeoutExpired:
            other_tunnel.kill()
            other_tunnel.wait(timeout=5)
