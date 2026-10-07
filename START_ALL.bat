@echo off
REM ================================================================
REM START_ALL.bat - One-click launcher for Digital Risk Protection Platform
REM ================================================================
REM This script starts all four modules in separate terminal windows.
REM 
REM Module 1 (M1) - Brand Registry          -> http://localhost:8000
REM Module 2 (M2) - Social Monitoring       -> http://localhost:8001
REM Module 3 (M3) - App Monitoring          -> http://localhost:8002
REM Module 4 (M4) - Unified Frontend        -> http://localhost:5173
REM ================================================================

REM Get the directory of this batch file (project root)
set "PROJECT_ROOT=%~dp0"
REM Remove trailing backslash
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo ================================================================
echo Digital Risk Protection Platform - Starting All Modules
echo ================================================================
echo Project Root: %PROJECT_ROOT%
echo.
echo Module 1 (M1) - Brand Registry        -> Port 8000
echo Module 2 (M2) - Social Monitoring     -> Port 8001
echo Module 3 (M3) - App Monitoring        -> Port 8002
echo Module 4 (M4) - Unified Frontend      -> Port 5173
echo ================================================================
echo.

REM Create temporary launcher scripts
set "TEMP_DIR=%TEMP%\drpp_launcher_%RANDOM%"
mkdir "%TEMP_DIR%" 2>nul

REM -----------------------------------------------------------------
REM Module 1 Launcher
REM -----------------------------------------------------------------
echo @echo off > "%TEMP_DIR%\launch_m1.bat"
echo cd /d "%PROJECT_ROOT%\module1\Digital-Risk-Protection-Platform-Inspestion-Module-1-main\backend" >> "%TEMP_DIR%\launch_m1.bat"
echo echo [M1] Starting Brand Registry on port 8000... >> "%TEMP_DIR%\launch_m1.bat"
echo python run.py >> "%TEMP_DIR%\launch_m1.bat"
echo pause >> "%TEMP_DIR%\launch_m1.bat"

REM -----------------------------------------------------------------
REM Module 2 Launcher
REM -----------------------------------------------------------------
echo @echo off > "%TEMP_DIR%\launch_m2.bat"
echo cd /d "%PROJECT_ROOT%\module2\module-2-main\backend" >> "%TEMP_DIR%\launch_m2.bat"
echo echo [M2] Starting Social Monitoring on port 8001... >> "%TEMP_DIR%\launch_m2.bat"
echo python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload >> "%TEMP_DIR%\launch_m2.bat"
echo pause >> "%TEMP_DIR%\launch_m2.bat"

REM -----------------------------------------------------------------
REM Module 3 Launcher
REM -----------------------------------------------------------------
echo @echo off > "%TEMP_DIR%\launch_m3.bat"
echo cd /d "%PROJECT_ROOT%\module3\module-3-app-store-monitoring-main\backend" >> "%TEMP_DIR%\launch_m3.bat"
echo echo [M3] Starting App Monitoring on port 8002... >> "%TEMP_DIR%\launch_m3.bat"
echo python run.py >> "%TEMP_DIR%\launch_m3.bat"
echo pause >> "%TEMP_DIR%\launch_m3.bat"

REM -----------------------------------------------------------------
REM Module 4 Launcher
REM -----------------------------------------------------------------
echo @echo off > "%TEMP_DIR%\launch_m4.bat"
echo cd /d "%PROJECT_ROOT%\module 4" >> "%TEMP_DIR%\launch_m4.bat"
echo echo [M4] Starting Unified Frontend on port 5173... >> "%TEMP_DIR%\launch_m4.bat"
echo npm run dev >> "%TEMP_DIR%\launch_m4.bat"
echo pause >> "%TEMP_DIR%\launch_m4.bat"

REM -----------------------------------------------------------------
REM Launch all modules in separate windows
REM -----------------------------------------------------------------
echo Starting Module 1 (M1) - Brand Registry on port 8000...
start "M1 - Brand Registry (Port 8000)" cmd /k "%TEMP_DIR%\launch_m1.bat"

echo Starting Module 2 (M2) - Social Monitoring on port 8001...
start "M2 - Social Monitoring (Port 8001)" cmd /k "%TEMP_DIR%\launch_m2.bat"

echo Starting Module 3 (M3) - App Monitoring on port 8002...
start "M3 - App Monitoring (Port 8002)" cmd /k "%TEMP_DIR%\launch_m3.bat"

echo Starting Module 4 (M4) - Unified Frontend on port 5173...
start "M4 - Unified Frontend (Port 5173)" cmd /k "%TEMP_DIR%\launch_m4.bat"

REM -----------------------------------------------------------------
echo.
echo ================================================================
echo All four modules started in separate terminal windows.
echo ================================================================
echo.
echo Module 1 (M1) - Brand Registry:      http://localhost:8000
echo Module 2 (M2) - Social Monitoring:   http://localhost:8001
echo Module 3 (M3) - App Monitoring:      http://localhost:8002
echo Module 4 (M4) - Unified Frontend:    http://localhost:5173
echo ================================================================
echo.
echo Health check endpoints:
echo   M1: http://localhost:8000/health
echo   M2: http://localhost:8001/health
echo   M3: http://localhost:8002/health
echo   M4: http://localhost:5173
echo ================================================================
echo.
echo To stop all services: Close the four terminal windows.
echo ================================================================

REM Optional: Open browser to M4 frontend after a brief delay
REM Uncomment the following lines if you want auto-browser open
REM timeout /t 5 /nobreak >nul
REM start "" "http://localhost:5173"

pause