[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$UvPath,
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,
    [string]$PluginDirectory = (Split-Path -Parent $PSScriptRoot),
    [string]$TaskName = 'EstudoJuridicoAvancadoIndexSync',
    [switch]$Confirm
)

$ErrorActionPreference = 'Stop'
$runnerPath = Join-Path $PSScriptRoot 'index_sync_runner.ps1'
if (-not $Confirm) {
    throw 'A instalação da verificação periódica exige -Confirm.'
}
if (-not (Test-Path -LiteralPath $runnerPath -PathType Leaf)) {
    throw "Runner de indexação não encontrado: $runnerPath"
}

$uv = (Get-Item -LiteralPath (Resolve-Path -LiteralPath $UvPath).Path).FullName
$config = (Get-Item -LiteralPath (Resolve-Path -LiteralPath $ConfigPath).Path).FullName
$plugin = (Get-Item -LiteralPath (Resolve-Path -LiteralPath $PluginDirectory).Path).FullName
if (-not (Test-Path -LiteralPath $uv -PathType Leaf)) {
    throw "uv precisa ser um arquivo: $uv"
}
if (-not (Test-Path -LiteralPath $config -PathType Leaf)) {
    throw "Configuração precisa ser um arquivo: $config"
}
if (-not (Test-Path -LiteralPath $plugin -PathType Container)) {
    throw "Plugin precisa ser uma pasta: $plugin"
}

$runtime = Join-Path $plugin '.runtime\index-sync'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
$powershell = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $powershell -PathType Leaf)) {
    $powershell = (Get-Command powershell.exe -ErrorAction Stop).Source
}
$arguments = '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass ' +
    "-File `"$runnerPath`" -UvPath `"$uv`" -ConfigPath `"$config`" " +
    "-PluginDirectory `"$plugin`" -RuntimeDirectory `"$runtime`""
$action = New-ScheduledTaskAction -Execute $powershell -Argument $arguments -WorkingDirectory $plugin
$identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$login = New-ScheduledTaskTrigger -AtLogOn -User $identity
$periodic = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) `
    -RepetitionInterval (New-TimeSpan -Minutes 10) `
    -RepetitionDuration (New-TimeSpan -Days 3650)
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
    -MultipleInstances IgnoreNew

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing -and [string]$existing.Actions.Arguments -notlike '*index_sync_runner.ps1*') {
    throw "Tarefa existente com outro propósito: $TaskName"
}
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger @($login, $periodic) `
    -Principal $principal `
    -Settings $settings `
    -Description 'Verifica alterações no acervo Markdown e encerra após sincronizar o índice.' `
    -Force | Out-Null
Write-Output "Verificação pontual instalada: $TaskName"
