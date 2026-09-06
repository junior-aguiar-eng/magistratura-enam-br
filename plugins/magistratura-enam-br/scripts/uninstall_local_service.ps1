[CmdletBinding()]
param([switch]$Confirm)

$ErrorActionPreference = 'Stop'
$serviceName = 'EstudoJuridicoAvancadoMcp'
$taskName = $serviceName
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$pluginRoot = Split-Path -Parent $PSScriptRoot
$runtimeDirectory = Join-Path $pluginRoot '.runtime\startup'
$runnerPath = Join-Path $runtimeDirectory 'runner.ps1'
$manifestPath = Join-Path $runtimeDirectory 'startup.json'
$runtimeProfilePath = Join-Path $runtimeDirectory 'tunnel-profile.yaml'
$pidPath = Join-Path $runtimeDirectory 'tunnel.pid'
$supervisorPidPath = Join-Path $runtimeDirectory 'supervisor.pid'
$stdoutLogPath = Join-Path $runtimeDirectory 'tunnel-client.stdout.log'
$stderrLogPath = Join-Path $runtimeDirectory 'tunnel-client.stderr.log'
$supervisorLogPath = Join-Path $runtimeDirectory 'supervisor.log'

if (-not $Confirm) {
    throw 'A remoção exige confirmação explícita: execute novamente com -Confirm.'
}

$scheduledTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($null -ne $scheduledTask) {
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$expectedClientPath = $null
$expectedRunnerPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'local_service_runner.ps1'))
if (Test-Path -LiteralPath $manifestPath) {
    $settings = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($settings.tunnel_client) {
        $expectedClientPath = [IO.Path]::GetFullPath([string]$settings.tunnel_client)
    }
}

if (Test-Path -LiteralPath $supervisorPidPath) {
    $savedSupervisorPid = (Get-Content -LiteralPath $supervisorPidPath -Raw).Trim()
    if ($savedSupervisorPid -match '^\d+$') {
        $supervisor = Get-CimInstance Win32_Process -Filter "ProcessId = $savedSupervisorPid"
        if (
            $null -ne $supervisor -and
            $supervisor.Name -in @('powershell.exe', 'pwsh.exe') -and
            $supervisor.CommandLine -and
            $supervisor.CommandLine.IndexOf($expectedRunnerPath, [StringComparison]::OrdinalIgnoreCase) -ge 0
        ) {
            Stop-Process -Id ([int]$savedSupervisorPid)
        }
    }
}

if (Test-Path -LiteralPath $pidPath) {
    $savedPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
    if ($savedPid -match '^\d+$') {
        $process = Get-Process -Id ([int]$savedPid) -ErrorAction SilentlyContinue
        $actualClientPath = if ($null -ne $process) { $process.Path } else { $null }
        if (
            $null -ne $process -and
            $process.ProcessName -eq 'tunnel-client' -and
            $expectedClientPath -and
            $actualClientPath -and
            ([IO.Path]::GetFullPath([string]$actualClientPath) -ieq $expectedClientPath)
        ) {
            Stop-Process -Id $process.Id
        }
    }
}

if (Test-Path -LiteralPath $runKey) {
    Remove-ItemProperty -Path $runKey -Name $serviceName -ErrorAction SilentlyContinue
}
foreach ($path in @(
    $pidPath,
    $supervisorPidPath,
    $runnerPath,
    $manifestPath,
    $runtimeProfilePath,
    $stdoutLogPath,
    $stderrLogPath,
    $supervisorLogPath
)) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path
    }
}

Write-Output 'Inicialização automática removida. A biblioteca e todos os dados de estudo foram preservados.'
