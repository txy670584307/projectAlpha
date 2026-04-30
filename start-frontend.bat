@echo off
REM ========================================
REM projectAlpha 前端启动脚本 (Windows)
REM ========================================

echo Starting projectAlpha Frontend...

cd /d "%~dp0frontend"

REM 检查 node_modules
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

REM 构建生产包（可选）
if "%1"=="build" (
    echo Building production bundle...
    call npm run build
    echo Build complete! Check dist/ directory.
    pause
    exit /b 0
)

REM 启动开发服务器
echo Starting frontend dev server...
call npm run dev

pause
