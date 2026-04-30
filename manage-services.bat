@echo off
REM ========================================
REM projectAlpha - Windows 服务管理脚本
REM ========================================
REM 用途: 启动/停止后端和前端服务
REM 用法: manage-services.bat [start|stop|restart|status]
REM ========================================

setlocal enabledelayedexpansion

set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend
set PID_FILE=%PROJECT_DIR%.services.pid
set LOG_DIR=%PROJECT_DIR%logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM === 函数: 启动服务 ===
:start_services
echo [INFO] 启动 projectAlpha 服务...

REM 启动后端服务
echo [INFO] 启动后端服务 (端口 8000)...
cd /d "%BACKEND_DIR%"
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
start /B uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level info > "%LOG_DIR%\backend.log" 2>&1
set BACKEND_PID=!ERRORLEVEL!
echo [INFO] 后端服务已启动

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端服务
echo [INFO] 启动前端服务 (端口 5173)...
cd /d "%FRONTEND_DIR%"
start /B npm run dev -- --host > "%LOG_DIR%\frontend.log" 2>&1
set FRONTEND_PID=!ERRORLEVEL!
echo [INFO] 前端服务已启动

REM 保存 PID
echo %BACKEND_PID% > "%PID_FILE%.backend"
echo %FRONTEND_PID% > "%PID_FILE%.frontend"

echo [INFO] 所有服务已启动
echo [INFO] 后端: http://127.0.0.1:8000
echo [INFO] 前端: http://localhost:5173
echo [INFO] API 文档: http://127.0.0.1:8000/docs
goto :eof

REM === 函数: 停止服务 ===
:stop_services
echo [INFO] 停止 projectAlpha 服务...

if exist "%PID_FILE%.backend" (
    set /p BACKEND_PID=<"%PID_FILE%.backend"
    taskkill /PID !BACKEND_PID! /F >nul 2>&1
    del "%PID_FILE%.backend"
    echo [INFO] 后端服务已停止
)

if exist "%PID_FILE%.frontend" (
    set /p FRONTEND_PID=<"%PID_FILE%.frontend"
    taskkill /PID !FRONTEND_PID! /F >nul 2>&1
    del "%PID_FILE%.frontend"
    echo [INFO] 前端服务已停止
)

REM 强制停止 uvicorn 和 node 进程
taskkill /IM uvicorn.exe /F >nul 2>&1
taskkill /IM node.exe /F >nul 2>&1

echo [INFO] 所有服务已停止
goto :eof

REM === 函数: 查看状态 ===
:show_status
echo [INFO] projectAlpha 服务状态:
echo.

REM 检查后端
curl -s http://127.0.0.1:8000/health >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo [OK] 后端服务运行中 - http://127.0.0.1:8000
) else (
    echo [FAIL] 后端服务未运行
)

REM 检查前端
curl -s http://localhost:5173 >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo [OK] 前端服务运行中 - http://localhost:5173
) else (
    echo [FAIL] 前端服务未运行
)
goto :eof

REM === 主逻辑 ===
if "%1"=="" (
    echo 用法: manage-services.bat [start^|stop^|restart^|status]
    echo.
    echo   start   - 启动后端和前端服务
    echo   stop    - 停止所有服务
    echo   restart - 重启所有服务
    echo   status  - 查看服务状态
    exit /b 1
)

if "%1"=="start" call :start_services
if "%1"=="stop" call :stop_services
if "%1"=="restart" (
    call :stop_services
    timeout /t 2 /nobreak >nul
    call :start_services
)
if "%1"=="status" call :show_status

endlocal
