import json
import shutil
import subprocess
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install_index_sync.ps1"
UNINSTALL = ROOT / "scripts" / "uninstall_index_sync.ps1"
RUNNER = ROOT / "scripts" / "index_sync_runner.ps1"
NAMESPACE = {"task": "http://schemas.microsoft.com/windows/2004/02/mit/task"}


@pytest.mark.skipif(shutil.which("powershell.exe") is None, reason="requer Windows")
@pytest.mark.parametrize("exit_code", [0, 2])
def test_runner_registra_saida_e_codigo_mesmo_com_stderr(
    tmp_path: Path, exit_code: int
) -> None:
    powershell = shutil.which("powershell.exe")
    assert powershell is not None
    fake_uv = tmp_path / "uv.cmd"
    fake_uv.write_text(
        f'@echo off\necho warning from uv 1>&2\necho {{"status":"unchanged"}}\nexit /b {exit_code}\n',
        encoding="ascii",
    )
    runtime = tmp_path / "runtime"

    executed = subprocess.run(
        [
            powershell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(RUNNER),
            "-UvPath",
            str(fake_uv),
            "-ConfigPath",
            str(tmp_path / "config.json"),
            "-PluginDirectory",
            str(tmp_path),
            "-RuntimeDirectory",
            str(runtime),
        ],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert executed.returncode == exit_code, executed.stderr
    record = json.loads((runtime / "last-run.json").read_text(encoding="utf-8-sig"))
    assert record["exit_code"] == exit_code
    assert "warning from uv" in record["result"]
    assert '"status":"unchanged"' in record["result"]


@pytest.mark.skipif(shutil.which("powershell.exe") is None, reason="requer Windows")
def test_instalador_registra_tarefa_pontual_no_login_e_a_cada_dez_minutos(
    tmp_path: Path,
) -> None:
    powershell = shutil.which("powershell.exe")
    uv = shutil.which("uv")
    assert powershell is not None
    assert uv is not None
    task_name = f"EstudoJuridicoIndexTest-{uuid.uuid4().hex}"
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    config_path = tmp_path / "library-config.json"
    config_path.write_text("{}", encoding="utf-8")

    try:
        installed = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(INSTALL),
                "-UvPath",
                uv,
                "-ConfigPath",
                str(config_path),
                "-PluginDirectory",
                str(plugin_dir),
                "-TaskName",
                task_name,
                "-Confirm",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert installed.returncode == 0, installed.stderr

        exported = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"Export-ScheduledTask -TaskName '{task_name}'",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert exported.returncode == 0, exported.stderr
        task = ET.fromstring(exported.stdout)
        assert task.find(".//task:LogonTrigger", NAMESPACE) is not None
        assert (
            task.find(
                ".//task:TimeTrigger/task:Repetition/task:Interval", NAMESPACE
            ).text
            == "PT10M"
        )
        assert (
            task.find(".//task:MultipleInstancesPolicy", NAMESPACE).text == "IgnoreNew"
        )
        arguments = task.find(
            ".//task:Actions/task:Exec/task:Arguments", NAMESPACE
        ).text
        assert "index_sync_runner.ps1" in arguments
        assert str(config_path) in arguments
    finally:
        subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"Unregister-ScheduledTask -TaskName '{task_name}' -Confirm:$false -ErrorAction SilentlyContinue",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )


@pytest.mark.skipif(shutil.which("powershell.exe") is None, reason="requer Windows")
def test_desinstalacao_remove_apenas_tarefa_e_preserva_indice(tmp_path: Path) -> None:
    powershell = shutil.which("powershell.exe")
    uv = shutil.which("uv")
    assert powershell is not None
    assert uv is not None
    task_name = f"EstudoJuridicoIndexTest-{uuid.uuid4().hex}"
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    config_path = tmp_path / "library-config.json"
    config_path.write_text("{}", encoding="utf-8")
    index_path = tmp_path / "biblioteca" / ".estudo-juridico" / "index.json"
    index_path.parent.mkdir(parents=True)
    index_path.write_text("dados preservados", encoding="utf-8")

    try:
        installed = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(INSTALL),
                "-UvPath",
                uv,
                "-ConfigPath",
                str(config_path),
                "-PluginDirectory",
                str(plugin_dir),
                "-TaskName",
                task_name,
                "-Confirm",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert installed.returncode == 0, installed.stderr

        removed = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(UNINSTALL),
                "-TaskName",
                task_name,
                "-Confirm",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        assert removed.returncode == 0, removed.stderr
        remaining = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"Get-ScheduledTask -TaskName '{task_name}' -ErrorAction SilentlyContinue",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert remaining.stdout.strip() == ""
        assert index_path.read_text(encoding="utf-8") == "dados preservados"
    finally:
        subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"Unregister-ScheduledTask -TaskName '{task_name}' -Confirm:$false -ErrorAction SilentlyContinue",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
