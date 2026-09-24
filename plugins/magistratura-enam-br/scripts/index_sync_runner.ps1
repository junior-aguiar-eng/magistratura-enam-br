[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$UvPath,
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,
    [Parameter(Mandatory = $true)]
    [string]$PluginDirectory,
    [Parameter(Mandatory = $true)]
    [string]$RuntimeDirectory
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $RuntimeDirectory -Force | Out-Null
$ErrorActionPreference = 'Continue'
try {
    $output = & $UvPath run --directory $PluginDirectory python -m mcp_server.index_sync --config $ConfigPath 2>&1
    $exitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = 'Stop'
}
@{
    checked_at = (Get-Date).ToUniversalTime().ToString('o')
    exit_code = $exitCode
    result = (@($output) -join "`n")
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $RuntimeDirectory 'last-run.json') -Encoding utf8
exit $exitCode
