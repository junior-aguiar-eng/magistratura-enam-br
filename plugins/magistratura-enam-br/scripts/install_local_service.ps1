[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TunnelClientPath,
    [Parameter(Mandatory = $true)]
    [string]$TunnelProfilePath,
    [string]$PluginDirectory = (Split-Path -Parent $PSScriptRoot),
    [switch]$Confirm
)

$ErrorActionPreference = 'Stop'
$serviceName = 'EstudoJuridicoAvancadoMcp'
$taskName = $serviceName
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$sourceRunnerPath = Join-Path $PSScriptRoot 'local_service_runner.ps1'

if (-not $Confirm) {
    throw 'A instalação exige confirmação explícita: execute novamente com -Confirm.'
}
if (-not (Test-Path -LiteralPath $sourceRunnerPath -PathType Leaf)) {
    throw "Runner supervisor não encontrado: $sourceRunnerPath"
}

$tunnelClientItem = Get-Item -LiteralPath (Resolve-Path -LiteralPath $TunnelClientPath).Path
if ($tunnelClientItem.PSIsContainer) {
    throw "Tunnel-client precisa ser um arquivo executável: $TunnelClientPath"
}
$tunnelClient = $tunnelClientItem.FullName

$tunnelProfileItem = Get-Item -LiteralPath (Resolve-Path -LiteralPath $TunnelProfilePath).Path
if ($tunnelProfileItem.PSIsContainer) {
    throw "O perfil do túnel precisa ser um arquivo: $TunnelProfilePath"
}
$tunnelProfile = $tunnelProfileItem.FullName

$pluginItem = Get-Item -LiteralPath (Resolve-Path -LiteralPath $PluginDirectory).Path
if (-not $pluginItem.PSIsContainer) {
    throw "O diretório do plugin precisa ser uma pasta: $PluginDirectory"
}
$pluginRoot = $pluginItem.FullName
$runtimeDirectory = Join-Path $pluginRoot '.runtime\startup'
$runtimeProfilePath = Join-Path $runtimeDirectory 'tunnel-profile.yaml'
$manifestPath = Join-Path $runtimeDirectory 'startup.json'
$runtimeKey = [Environment]::GetEnvironmentVariable('CONTROL_PLANE_API_KEY', 'User')
if ([string]::IsNullOrWhiteSpace($runtimeKey)) {
    throw 'CONTROL_PLANE_API_KEY precisa existir no ambiente do usuário; nenhum segredo será gravado pelo instalador.'
}

New-Item -ItemType Directory -Path $runtimeDirectory -Force | Out-Null
Copy-Item -LiteralPath $tunnelProfile -Destination $runtimeProfilePath -Force
@{
    tunnel_client = $tunnelClient
    tunnel_profile = $runtimeProfilePath
    working_directory = $pluginRoot
} | ConvertTo-Json | Set-Content -LiteralPath $manifestPath -Encoding utf8

$powershell = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $powershell)) {
    $powershell = (Get-Command powershell.exe -ErrorAction Stop).Source
}
$actionArguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$sourceRunnerPath`" -TunnelClientPath `"$tunnelClient`" -TunnelProfilePath `"$runtimeProfilePath`" -WorkingDirectory `"$pluginRoot`" -RuntimeDirectory `"$runtimeDirectory`""
$action = New-ScheduledTaskAction `
    -Execute $powershell `
    -Argument $actionArguments
$identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$taskSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $taskSettings `
    -Description 'Mantém o túnel MCP do Estudo Jurídico Avançado disponível.' `
    -Force | Out-Null

if (Test-Path -LiteralPath $runKey) {
    Remove-ItemProperty -Path $runKey -Name $serviceName -ErrorAction SilentlyContinue
}
Start-ScheduledTask -TaskName $taskName
Write-Output "Inicialização automática instalada no escopo do usuário: $serviceName"
