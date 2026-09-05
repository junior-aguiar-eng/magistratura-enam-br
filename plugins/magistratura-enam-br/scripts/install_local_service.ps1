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
$runnerPath = Join-Path $runtimeDirectory 'runner.ps1'
$manifestPath = Join-Path $runtimeDirectory 'startup.json'

if (-not $Confirm) {
    throw 'A instalação exige confirmação explícita: execute novamente com -Confirm.'
}

$tunnelClient = (Resolve-Path -LiteralPath $TunnelClientPath).Path
$tunnelProfile = (Resolve-Path -LiteralPath $TunnelProfilePath).Path
$pluginRoot = (Resolve-Path -LiteralPath $PluginDirectory).Path
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

@'
$ErrorActionPreference = 'Stop'
$startupDirectory = Split-Path -Parent $PSCommandPath
$settings = Get-Content -LiteralPath (Join-Path $startupDirectory 'startup.json') -Raw | ConvertFrom-Json
$quotedProfile = '"' + $settings.tunnel_profile + '"'
$process = Start-Process -FilePath $settings.tunnel_client `
    -ArgumentList @('run', '--config', $quotedProfile) `
    -WorkingDirectory $settings.working_directory `
    -WindowStyle Hidden `
    -PassThru
Set-Content -LiteralPath (Join-Path $startupDirectory 'tunnel.pid') -Value $process.Id -Encoding ascii
'@ | Set-Content -LiteralPath $runnerPath -Encoding utf8

$powershell = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $powershell)) {
    $powershell = (Get-Command powershell.exe -ErrorAction Stop).Source
}
$runCommand = '"{0}" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{1}"' -f $powershell, $runnerPath
New-Item -Path $runKey -Force | Out-Null
Set-ItemProperty -Path $runKey -Name $serviceName -Value $runCommand

& $runnerPath
Write-Output "Inicialização automática instalada no escopo do usuário: $serviceName"
