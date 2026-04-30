@echo off
REM ============================================
REM Windows Service Registration Script
REM Registers projectAlpha backend as a Windows service using NSSM
REM ============================================

echo ========================================
echo projectAlpha Backend Service Installer
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: Please run this script as Administrator
    pause
    exit /b 1
)

REM Configuration - modify these paths as needed
set PROJECT_DIR=C:\projectalpha
set BACKEND_DIR=%PROJECT_DIR%\backend
set PYTHON_DIR=C:\Python312
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set VENV_PYTHON=%BACKEND_DIR%\venv\Scripts\python.exe
set SERVICE_NAME=projectalpha-backend

REM Check if NSSM is installed
where nssm >nul 2>&1
if %errorLevel% neq 0 (
    echo NSSM is not installed.
    echo Please download NSSM from https://nssm.cc/download
    echo and add it to your system PATH.
    pause
    exit /b 1
)

REM Check if Python exists
if not exist "%VENV_PYTHON%" (
    echo Python virtual environment not found at:
    echo %VENV_PYTHON%
    echo.
    echo Please run the setup script first to create the virtual environment.
    pause
    exit /b 1
)

echo Installing %SERVICE_NAME% service...
echo.

REM Remove existing service if exists
nssm status %SERVICE_NAME% >nul 2>&1
if %errorLevel% equ 0 (
    echo Service already exists. Removing...
    nssm stop %SERVICE_NAME% >nul 2>&1
    nssm remove %SERVICE_NAME% confirm
    echo.
)

REM Install service
nssm install %SERVICE_NAME% "%VENV_PYTHON%"
nssm set %SERVICE_NAME% AppDirectory "%BACKEND_DIR%"
nssm set %SERVICE_NAME% AppParameters "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4"
nssm set %SERVICE_NAME% Environment ENV_FILE=.env.production
nssm set %SERVICE_NAME% AppStdout "%BACKEND_DIR%\logs\stdout.log"
nssm set %SERVICE_NAME% AppStderr "%BACKEND_DIR%\logs\stderr.log"
nssm set %SERVICE_NAME% AppRotateFiles 1
nssm set %SERVICE_NAME% AppRotateBytes 10485760
nssm set %SERVICE_NAME% AppRotateLines 0
nssm set %SERVICE_NAME% AppRotateOnline 1
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START

echo.
echo Starting service...
nssm start %SERVICE_NAME%

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo Service installed and started successfully!
    echo.
    echo Service Name: %SERVICE_NAME%
    echo API URL: http://localhost:8000
    echo Health Check: http://localhost:8000/health
    echo.
    echo Management commands:
    echo   nssm status %SERVICE_NAME%
    echo   nssm stop %SERVICE_NAME%
    echo   nssm restart %SERVICE_NAME%
    echo   nssm remove %SERVICE_NAME% confirm
    echo ========================================
) else (
    echo.
    echo Service installation failed. Check the error messages above.
)

pause
