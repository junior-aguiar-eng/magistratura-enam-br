[CmdletBinding()]
param(
    [switch]$InstalarDependencias
)

$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$marketplace = 'magistratura-enam-br'
$plugin = 'magistratura-enam-br'
$manifesto = Join-Path $raiz '.agents\plugins\marketplace.json'
$fontePlugin = Join-Path $raiz 'plugins\magistratura-enam-br\.codex-plugin\plugin.json'

if (-not (Test-Path -LiteralPath $manifesto)) {
    throw "Marketplace ausente: $manifesto"
}
if (-not (Test-Path -LiteralPath $fontePlugin)) {
    throw "Plugin ausente ou incompleto: $fontePlugin"
}
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw 'Codex CLI não foi encontrado. Instale ou atualize o Codex e execute novamente.'
}

$configurados = (& codex plugin marketplace list 2>&1 | Out-String)
$padrao = '(?m)^Marketplace `' + [regex]::Escape($marketplace) + '`'
if ($configurados -notmatch $padrao) {
    & codex plugin marketplace add $raiz --json
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível registrar a marketplace local.' }
}

& codex plugin add "$plugin@$marketplace" --json
if ($LASTEXITCODE -ne 0) { throw 'Não foi possível instalar o plugin.' }

if ($InstalarDependencias) {
    $requisitos = Join-Path $raiz 'plugins\magistratura-enam-br\requirements.txt'
    $py = Get-Command py -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
    if (-not $py) { throw 'Python não foi encontrado para instalar as dependências opcionais dos scripts.' }
    & $py.Source -m pip install --user -r $requisitos
    if ($LASTEXITCODE -ne 0) { throw 'A instalação das dependências Python não foi concluída.' }
}

Write-Host "Plugin $plugin instalado. Abra uma nova tarefa no Codex para usar as skills."
