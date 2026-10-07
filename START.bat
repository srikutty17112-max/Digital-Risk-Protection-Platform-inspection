@echo off
chcp 65001 >nul
title AI-Powered Digital Risk Protection Platform

echo ============================================
echo AI-Powered Digital Risk Protection Platform
echo ============================================
echo.
echo Starting unified backend (port 8000)...
start "DRPP Backend" cmd /c "cd /d "%~dp0backend" && python run.py"

timeout /t 3 /nobreak >nul

echo Starting frontend (port 5173)...
start "DRPP Frontend" cmd /c "cd /d "%~dp0module 4" && npm run dev"

echo.
echo Platform starting...
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause
