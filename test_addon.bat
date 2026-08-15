@echo off
setlocal enabledelayedexpansion
title Anki Wykiati Toolkit - Test, Clean, Build & Preview
color 0b

:MENU
cls
echo ===============================================================================
echo                ANKI WYKIATI TOOLKIT - CONTROL PANEL & TEST RUNNER
echo ===============================================================================
echo.
echo   [1] Run All 38 Automated Unit Tests (Headless)
echo   [2] Build Clean .ankiaddon Release Package
echo   [3] Start Local HTTP Webhook Bridge Server (127.0.0.1:8765)
echo   [4] Send Sample Image Card via PowerShell Webhook
echo   [5] Clean Old Addon Versions and Install Fresh Copy into Anki
echo   [6] Open iOS Liquid Glass Live Web Preview (preview.html)
echo   [7] Launch Standalone Native Qt Window Preview (preview_ui.py)
echo   [8] Exit
echo.
echo ===============================================================================
set /p OPTION=" Choose an option [1-8]: "

if "%OPTION%"=="1" goto RUN_TESTS
if "%OPTION%"=="2" goto BUILD_PACKAGE
if "%OPTION%"=="3" goto RUN_BRIDGE
if "%OPTION%"=="4" goto SEND_TEST_CARD
if "%OPTION%"=="5" goto CLEAN_AND_INSTALL_ANKI
if "%OPTION%"=="6" goto OPEN_HTML_PREVIEW
if "%OPTION%"=="7" goto OPEN_QT_PREVIEW
if "%OPTION%"=="8" goto EXIT_SCRIPT

echo Invalid option!
timeout /t 2 >nul
goto MENU

:RUN_TESTS
cls
echo ===============================================================================
echo  Executing Full Automated Test Suite...
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
echo  Building .ankiaddon Distributable Package...
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
echo  Starting Local HTTP Webhook Bridge on http://127.0.0.1:8765 ...
echo  (Press Ctrl+C to terminate the server)
echo ===============================================================================
echo.
python -c "import sys, os; sys.path.insert(0, os.path.abspath('anki-addon')); from discord.client import HttpBridgeServer; import time; server = HttpBridgeServer('127.0.0.1', 8765); server.start(); print('[OK] Server is Active and listening on port 8765.'); [time.sleep(1) for _ in iter(int, 1)]"
echo.
pause
goto MENU

:SEND_TEST_CARD
cls
echo ===============================================================================
echo  Sending Sample Image Card via PowerShell to Local Webhook...
echo ===============================================================================
echo.
powershell -Command "$body = @{ image_url = 'https://picsum.photos/400/300'; caption = 'Human Heart Anatomy'; deck = 'Medicine::Cardiology' } | ConvertTo-Json; try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/card' -Method Post -ContentType 'application/json' -Body $body; Write-Host 'Server Response:' -ForegroundColor Green; $res | Format-Custom } catch { Write-Host 'Connection Error. Is the HTTP Bridge Server running? (Option 3)' -ForegroundColor Red; Write-Host $_ }"
echo.
echo ===============================================================================
pause
goto MENU

:CLEAN_AND_INSTALL_ANKI
cls
echo ===============================================================================
echo  Cleaning Legacy Addon Versions and Installing Clean Copy into Anki...
echo ===============================================================================
echo.
set "ANKI_BASE_DIR=%APPDATA%\Anki2\addons21"

if not exist "%ANKI_BASE_DIR%" (
    echo [WARNING] Anki addons directory not found at: %ANKI_BASE_DIR%
    echo Please make sure Anki has been launched at least once on this computer.
    pause
    goto MENU
)

echo [1/3] Searching and removing older or duplicate versions...
if exist "%ANKI_BASE_DIR%\anki_discord_toolkit" (
    echo   - Removing legacy folder: %ANKI_BASE_DIR%\anki_discord_toolkit
    rmdir /s /q "%ANKI_BASE_DIR%\anki_discord_toolkit"
)
if exist "%ANKI_BASE_DIR%\anki-addon" (
    echo   - Removing legacy folder: %ANKI_BASE_DIR%\anki-addon
    rmdir /s /q "%ANKI_BASE_DIR%\anki-addon"
)
if exist "%ANKI_BASE_DIR%\anki_wykiati_addon" (
    echo   - Removing legacy folder: %ANKI_BASE_DIR%\anki_wykiati_addon
    rmdir /s /q "%ANKI_BASE_DIR%\anki_wykiati_addon"
)
if exist "%ANKI_BASE_DIR%\anki_wykiati_toolkit" (
    echo   - Removing existing folder: %ANKI_BASE_DIR%\anki_wykiati_toolkit
    rmdir /s /q "%ANKI_BASE_DIR%\anki_wykiati_toolkit"
)

echo [2/3] Copying fresh files to: %ANKI_BASE_DIR%\anki_wykiati_toolkit ...
xcopy /e /i /y "anki-addon" "%ANKI_BASE_DIR%\anki_wykiati_toolkit"

echo.
echo [3/3] Success! Anki Wykiati Toolkit is cleanly installed.
echo Restart Anki to see the new Full Black theme and 'Anki Wykiati Toolkit' menu.
echo.
pause
goto MENU

:OPEN_HTML_PREVIEW
cls
echo ===============================================================================
echo  Opening iOS Liquid Glass Interactive Web Preview...
echo ===============================================================================
echo.
start "" "preview.html"
echo [OK] Opened preview.html in your default web browser.
echo.
pause
goto MENU

:OPEN_QT_PREVIEW
cls
echo ===============================================================================
echo  Launching Native Desktop Qt Preview Window...
echo ===============================================================================
echo.
python preview_ui.py
echo.
pause
goto MENU

:EXIT_SCRIPT
echo Exiting...
exit /b 0
