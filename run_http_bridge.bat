@echo off
title Anki Discord Toolkit - HTTP Bridge Server
color 0a
cls
echo ===============================================================================
echo               ANKI DISCORD TOOLKIT - HTTP WEBHOOK BRIDGE
echo ===============================================================================
echo.
echo  Iniciando Servidor HTTP Bridge em: http://127.0.0.1:8765
echo  Endpoint de recebimento: POST http://127.0.0.1:8765/api/card
echo  Status / Health check:  GET  http://127.0.0.1:8765/health
echo.
echo  Pressione Ctrl+C para encerrar o servidor a qualquer momento.
echo ===============================================================================
echo.
python -c "import sys, os; sys.path.insert(0, os.path.abspath('anki-addon')); from discord.client import HttpBridgeServer; import time; server = HttpBridgeServer('127.0.0.1', 8765); server.start(); print('[INFO] Servidor Ativo e pronto para receber cartoes.'); [time.sleep(1) for _ in iter(int, 1)]"
pause
