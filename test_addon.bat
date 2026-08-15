@echo off
setlocal enabledelayedexpansion
title Anki Wykiati Toolkit - Test, Preview & Build Runner
color 0b

:MENU
cls
echo ===============================================================================
echo                ANKI WYKIATI TOOLKIT - PAINEL DE CONTROLE E TESTES
echo ===============================================================================
echo.
echo   [1] Executar Todos os Testes Unitarios Automatizados (38 Testes)
echo   [2] Gerar Pacote Distribuivel .ankiaddon (Pasta release/)
echo   [3] Iniciar Servidor HTTP Bridge Local (Modo Teste Standalone)
echo   [4] Enviar Cartao de Teste com Imagem via Webhook Local (PowerShell)
echo   [5] Instalar Add-on Diretamente no Anki Local (%APPDATA%\Anki2)
echo   [6] Visualizar Preview do Design iOS Liquid Glass no Navegador (preview.html)
echo   [7] Abrir Preview Nativo em Janela Qt (preview_ui.py)
echo   [8] Sair
echo.
echo ===============================================================================
set /p OPTION=" Escolha uma opcao [1-8]: "

if "%OPTION%"=="1" goto RUN_TESTS
if "%OPTION%"=="2" goto BUILD_PACKAGE
if "%OPTION%"=="3" goto RUN_BRIDGE
if "%OPTION%"=="4" goto SEND_TEST_CARD
if "%OPTION%"=="5" goto INSTALL_ANKI
if "%OPTION%"=="6" goto OPEN_HTML_PREVIEW
if "%OPTION%"=="7" goto OPEN_QT_PREVIEW
if "%OPTION%"=="8" goto EXIT_SCRIPT

echo Opcao invalida!
timeout /t 2 >nul
goto MENU

:RUN_TESTS
cls
echo ===============================================================================
echo  Executando Suite de Testes Unitarios do Anki Wykiati Toolkit...
echo ===============================================================================
echo.
python -m unittest discover -s anki-addon/tests -p "test_*.py" -v
echo.
echo ===============================================================================
pause
goto MENU

:BUILD_PACKAGE
cls
echo ===============================================================================
echo  Construindo Pacote .ankiaddon...
echo ===============================================================================
echo.
python package_addon.py
echo.
echo ===============================================================================
pause
goto MENU

:RUN_BRIDGE
cls
echo ===============================================================================
echo  Iniciando Servidor HTTP Webhook Bridge em http://127.0.0.1:8765 ...
echo  (Pressione Ctrl+C para encerrar o servidor)
echo ===============================================================================
echo.
python -c "import sys, os; sys.path.insert(0, os.path.abspath('anki-addon')); from discord.client import HttpBridgeServer; import time; server = HttpBridgeServer('127.0.0.1', 8765); server.start(); print('Servidor Ativo! Pressione Ctrl+C para parar.'); [time.sleep(1) for _ in iter(int, 1)]"
echo.
pause
goto MENU

:SEND_TEST_CARD
cls
echo ===============================================================================
echo  Enviando Cartao com Imagem para o Servidor Local via PowerShell...
echo ===============================================================================
echo.
powershell -Command "$body = @{ image_url = 'https://picsum.photos/400/300'; caption = 'Diagrama de Teste do Coracao'; deck = 'Medicina::Cardiologia' } | ConvertTo-Json; try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/card' -Method Post -ContentType 'application/json' -Body $body; Write-Host 'Resposta do Servidor:' -ForegroundColor Green; $res | Format-Custom } catch { Write-Host 'Erro ao conectar. O servidor HTTP bridge esta rodando? (Opcao 3)' -ForegroundColor Red; Write-Host $_ }"
echo.
echo ===============================================================================
pause
goto MENU

:INSTALL_ANKI
cls
echo ===============================================================================
echo  Instalando Add-on na Pasta de Complementos do Anki Local...
echo ===============================================================================
echo.
set "ANKI_ADDONS_DIR=%APPDATA%\Anki2\addons21\anki_discord_toolkit"
if not exist "%APPDATA%\Anki2\addons21" (
    echo [AVISO] Pasta do Anki nao encontrada em %APPDATA%\Anki2\addons21
    echo Certifique-se de que o Anki ja foi aberto ao menos uma vez neste computador.
    pause
    goto MENU
)

echo Copiando arquivos para: %ANKI_ADDONS_DIR% ...
if exist "%ANKI_ADDONS_DIR%" rmdir /s /q "%ANKI_ADDONS_DIR%"
xcopy /e /i /y "anki-addon" "%ANKI_ADDONS_DIR%"
echo.
echo [SUCESSO] Anki Wykiati Toolkit instalado localmente com sucesso!
echo Reinicie o seu Anki para visualizar o menu 'Anki Discord Toolkit' sob 'Ferramentas'.
echo.
pause
goto MENU

:OPEN_HTML_PREVIEW
cls
echo ===============================================================================
echo  Abrindo Preview Interativo do Design iOS Liquid Glass no Navegador...
echo ===============================================================================
echo.
start "" "preview.html"
echo [OK] O arquivo preview.html foi aberto no seu navegador padrao.
echo.
pause
goto MENU

:OPEN_QT_PREVIEW
cls
echo ===============================================================================
echo  Abrindo Janela de Preview Nativo Qt (preview_ui.py)...
echo ===============================================================================
echo.
python preview_ui.py
echo.
pause
goto MENU

:EXIT_SCRIPT
echo Saindo...
exit /b 0
