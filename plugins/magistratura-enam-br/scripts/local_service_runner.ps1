[CmdletBinding()]
param(
    [string]$TunnelClientPath,
    [string]$TunnelProfilePath,
    [string]$WorkingDirectory,
    [string]$RuntimeDirectory,
    [ValidateRange(0, 300)]
    [int]$RestartDelaySeconds = 5,
    [ValidateRange(0, 1000)]
    [int]$MaxStarts = 0,
    [string]$MutexName = 'Local\EstudoJuridicoAvancadoMcpSupervisor'
)

$ErrorActionPreference = 'Stop'
$startupDirectory = if ([string]::IsNullOrWhiteSpace($RuntimeDirectory)) {
    Split-Path -Parent $PSCommandPath
}
else {
    [IO.Path]::GetFullPath($RuntimeDirectory)
}
New-Item -ItemType Directory -Path $startupDirectory -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($TunnelClientPath)) {
    $settingsPath = Join-Path $startupDirectory 'startup.json'
    $settings = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
    $TunnelClientPath = [string]$settings.tunnel_client
    $TunnelProfilePath = [string]$settings.tunnel_profile
    $WorkingDirectory = [string]$settings.working_directory
}
if (
    [string]::IsNullOrWhiteSpace($TunnelClientPath) -or
    [string]::IsNullOrWhiteSpace($TunnelProfilePath) -or
    [string]::IsNullOrWhiteSpace($WorkingDirectory)
) {
    throw 'TunnelClientPath, TunnelProfilePath e WorkingDirectory precisam ser informados em conjunto.'
}

$clientPath = [IO.Path]::GetFullPath($TunnelClientPath)
$profilePath = [IO.Path]::GetFullPath($TunnelProfilePath)
$workingDirectory = [IO.Path]::GetFullPath($WorkingDirectory)
$stdoutPath = Join-Path $startupDirectory 'tunnel-client.stdout.log'
$stderrPath = Join-Path $startupDirectory 'tunnel-client.stderr.log'
$supervisorLogPath = Join-Path $startupDirectory 'supervisor.log'
$pidPath = Join-Path $startupDirectory 'tunnel.pid'
$supervisorPidPath = Join-Path $startupDirectory 'supervisor.pid'

if (-not (Test-Path -LiteralPath $clientPath -PathType Leaf)) {
    throw "Tunnel-client não encontrado: $clientPath"
}
if (-not (Test-Path -LiteralPath $profilePath -PathType Leaf)) {
    throw "Perfil do túnel não encontrado: $profilePath"
}
if (-not (Test-Path -LiteralPath $workingDirectory -PathType Container)) {
    throw "Diretório de trabalho não encontrado: $workingDirectory"
}

function Write-SupervisorLog {
    param([string]$Message)
    Add-Content -LiteralPath $supervisorLogPath -Value "$(Get-Date -Format o) $Message" -Encoding utf8
}

$mutex = [Threading.Mutex]::new($false, $MutexName)
$ownsMutex = $false
try {
    try {
        $ownsMutex = $mutex.WaitOne(0)
    }
    catch [Threading.AbandonedMutexException] {
        $ownsMutex = $true
    }
    if (-not $ownsMutex) {
        exit 0
    }

    Set-Content -LiteralPath $supervisorPidPath -Value $PID -Encoding ascii
    Write-SupervisorLog "supervisor started pid=$PID"
    $starts = 0

    while ($true) {
        $running = @(Get-CimInstance Win32_Process -Filter "Name = 'tunnel-client.exe'" |
            Where-Object {
                $_.ExecutablePath -and
                ([IO.Path]::GetFullPath([string]$_.ExecutablePath) -ieq $clientPath)
            })

        if ($running.Count -gt 0) {
            $tunnelPid = [int]$running[0].ProcessId
            Write-SupervisorLog "attached tunnel pid=$tunnelPid"
        }
        else {
            $quotedProfile = '"' + $profilePath + '"'
            $process = Start-Process -FilePath $clientPath `
                -ArgumentList @('run', '--config', $quotedProfile) `
                -WorkingDirectory $workingDirectory `
                -WindowStyle Hidden `
                -RedirectStandardOutput $stdoutPath `
                -RedirectStandardError $stderrPath `
                -PassThru
            $tunnelPid = $process.Id
            $starts += 1
            Write-SupervisorLog "started tunnel pid=$tunnelPid attempt=$starts"
        }

        Set-Content -LiteralPath $pidPath -Value $tunnelPid -Encoding ascii
        Wait-Process -Id $tunnelPid -ErrorAction SilentlyContinue
        Write-SupervisorLog "tunnel exited pid=$tunnelPid"

        if (Test-Path -LiteralPath $pidPath) {
            $recordedPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
            if ($recordedPid -eq [string]$tunnelPid) {
                Remove-Item -LiteralPath $pidPath
            }
        }
        if ($MaxStarts -gt 0 -and $starts -ge $MaxStarts) {
            break
        }
        if ($RestartDelaySeconds -gt 0) {
            Start-Sleep -Seconds $RestartDelaySeconds
        }
    }
}
finally {
    if ($ownsMutex) {
        if (Test-Path -LiteralPath $supervisorPidPath) {
            $recordedSupervisorPid = (Get-Content -LiteralPath $supervisorPidPath -Raw).Trim()
            if ($recordedSupervisorPid -eq [string]$PID) {
                Remove-Item -LiteralPath $supervisorPidPath
            }
        }
        $mutex.ReleaseMutex()
    }
    $mutex.Dispose()
}
