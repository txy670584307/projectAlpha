@echo off
REM ========================================
REM projectAlpha 后端启动脚本 (Windows)
REM ========================================

echo Starting projectAlpha Backend...

cd /d "%~dp0backend"

REM 检查虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    pause
    exit /b 1
)

REM 检查配置文件
if not exist .env (
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
    ) else (
        echo .env file not found!
        pause
        exit /b 1
    )
)

REM 执行数据库迁移
echo Running database migrations...
alembic upgrade head

REM 启动后端服务
echo Starting backend server on %API_HOST%:%API_PORT%...
uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
