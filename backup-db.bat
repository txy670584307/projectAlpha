@echo off
REM ========================================
REM projectAlpha - 数据库备份脚本
REM 用途: 备份 PostgreSQL 数据库到本地
REM 用法: backup-db.bat [数据库名]
REM ========================================

setlocal enabledelayedexpansion

set PGPASSWORD=projectalpha_pass
set PGUSER=projectalpha_user
set PGHOST=localhost
set PGPORT=5432
set DB_NAME=%~1
if "%DB_NAME%"=="" set DB_NAME=projectalpha

set PSQL_PATH=C:\Program Files\PostgreSQL\18\bin
set BACKUP_DIR=%~dp0backups
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=!TIMESTAMP: =0!
set BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_!TIMESTAMP!.sql

REM 创建备份目录
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo ========================================
echo projectAlpha 数据库备份
echo ========================================
echo 数据库: %DB_NAME%
echo 目标文件: %BACKUP_FILE%
echo.

REM 执行备份
"%PSQL_PATH%\pg_dump.exe" -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %DB_NAME% -f "%BACKUP_FILE%"

if !ERRORLEVEL! equ 0 (
    echo [OK] 备份完成: %BACKUP_FILE%
    
    REM 显示文件大小
    for %%A in ("%BACKUP_FILE%") do (
        echo [INFO] 文件大小: %%~zA 字节
    )
    
    REM 清理 7 天前的备份文件
    echo [INFO] 清理 7 天前的备份...
    forfiles /p "%BACKUP_DIR%" /m "%DB_NAME%_*.sql" /d -7 /c "cmd /c del @path" 2>nul
    echo [OK] 清理完成
) else (
    echo [FAIL] 备份失败!
    exit /b 1
)

endlocal
pause
