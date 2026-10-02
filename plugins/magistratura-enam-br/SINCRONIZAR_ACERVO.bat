@echo off
setlocal

for %%I in ("%~dp0.") do set "PLUGIN_DIR=%%~fI"
set "CONFIG_PATH=%~1"
if not defined CONFIG_PATH set "CONFIG_PATH=%PLUGIN_DIR%\.runtime\library-config.json"

if not exist "%CONFIG_PATH%" (
    echo Arquivo de configuracao nao encontrado: "%CONFIG_PATH%"
    goto :failure
)

set "UV_PATH=%USERPROFILE%\.local\bin\uv.exe"
if not exist "%UV_PATH%" (
    set "UV_PATH="
    for %%I in (uv.exe) do set "UV_PATH=%%~$PATH:I"
)
if not defined UV_PATH (
    echo uv.exe nao encontrado.
    goto :failure
)

"%UV_PATH%" run --directory "%PLUGIN_DIR%" python -m mcp_server.index_sync --config "%CONFIG_PATH%"
if errorlevel 1 goto :failure

echo.
echo Verificacao concluida.
pause
exit /b 0

:failure
echo.
echo Verificacao nao concluida. Consulte a mensagem acima.
pause
exit /b 1
