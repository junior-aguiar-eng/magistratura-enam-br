[CmdletBinding()]
param([switch]$Confirm)

$ErrorActionPreference = 'Stop'
$serviceName = 'EstudoJuridicoAvancadoMcp'
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$runtimeDirectory = Join-Path $env:LOCALAPPDATA 'Estudo Jurídico Avançado\startup'
$runnerPath = Join-Path $runtimeDirectory 'runner.ps1'
$manifestPath = Join-Path $runtimeDirectory 'startup.json'
$pidPath = Join-Path $runtimeDirectory 'tunnel.pid'

if (-not $Confirm) {
    throw 'A remoção exige confirmação explícita: execute novamente com -Confirm.'
}

if (Test-Path -LiteralPath $pidPath) {
    $savedPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
    if ($savedPid -match '^\d+$') {
        $process = Get-Process -Id ([int]$savedPid) -ErrorAction SilentlyContinue
        if ($null -ne $process -and $process.ProcessName -eq 'tunnel-client') {
            Stop-Process -Id $process.Id
        }
    }
}

if (Test-Path -LiteralPath $runKey) {
    Remove-ItemProperty -Path $runKey -Name $serviceName -ErrorAction SilentlyContinue
}
foreach ($path in @($pidPath, $runnerPath, $manifestPath)) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path
    }
}

Write-Output 'Inicialização automática removida. A biblioteca e todos os dados de estudo foram preservados.'
