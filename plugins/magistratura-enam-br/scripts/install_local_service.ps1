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
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$runtimeDirectory = Join-Path $env:LOCALAPPDATA 'Estudo Jurídico Avançado\startup'
$sourceRunnerPath = Join-Path $PSScriptRoot 'local_service_runner.ps1'
$runnerPath = Join-Path $runtimeDirectory 'runner.ps1'
$manifestPath = Join-Path $runtimeDirectory 'startup.json'

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
$runtimeKey = [Environment]::GetEnvironmentVariable('CONTROL_PLANE_API_KEY', 'User')
if ([string]::IsNullOrWhiteSpace($runtimeKey)) {
    throw 'CONTROL_PLANE_API_KEY precisa existir no ambiente do usuário; nenhum segredo será gravado pelo instalador.'
}

New-Item -ItemType Directory -Path $runtimeDirectory -Force | Out-Null
@{
    tunnel_client = $tunnelClient
    tunnel_profile = $tunnelProfile
    working_directory = $pluginRoot
} | ConvertTo-Json | Set-Content -LiteralPath $manifestPath -Encoding utf8
Copy-Item -LiteralPath $sourceRunnerPath -Destination $runnerPath -Force

$powershell = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $powershell)) {
    $powershell = (Get-Command powershell.exe -ErrorAction Stop).Source
}
$runCommand = '"{0}" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{1}"' -f $powershell, $runnerPath
New-Item -Path $runKey -Force | Out-Null
Set-ItemProperty -Path $runKey -Name $serviceName -Value $runCommand

$quotedRunner = '"' + $runnerPath + '"'
Start-Process -FilePath $powershell `
    -ArgumentList @('-NoProfile', '-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass', '-File', $quotedRunner) `
    -WorkingDirectory $runtimeDirectory `
    -WindowStyle Hidden
Write-Output "Inicialização automática instalada no escopo do usuário: $serviceName"
