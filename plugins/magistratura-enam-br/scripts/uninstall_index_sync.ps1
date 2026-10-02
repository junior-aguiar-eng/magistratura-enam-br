[CmdletBinding()]
param(
    [string]$TaskName = 'EstudoJuridicoAvancadoIndexSync',
    [switch]$Confirm
)

$ErrorActionPreference = 'Stop'
if (-not $Confirm) {
    throw 'A remoção da verificação periódica exige -Confirm.'
}

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Output "Tarefa já ausente: $TaskName"
    exit 0
}
if ([string]$task.Actions.Arguments -notlike '*index_sync_runner.ps1*') {
    throw "A tarefa não pertence ao verificador deste plugin: $TaskName"
}
if ($task.State -eq 'Running') {
    Stop-ScheduledTask -TaskName $TaskName
}
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Output "Verificação pontual removida: $TaskName"
