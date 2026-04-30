@echo off
REM ============================================
REM Database Backup Script for projectAlpha
REM PostgreSQL 数据库定时备份脚本 (Windows)
REM ============================================

SET PGPASSWORD=your_password
SET BACKUP_DIR=C:\projectalpha\backups
SET TIMESTAMP=%DATE:/=-%_%TIME::=-%
SET TIMESTAMP=%TIMESTAMP: =%
SET BACKUP_FILE=%BACKUP_DIR%\projectalpha_%TIMESTAMP%.sql

IF NOT EXIST "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
)

echo Starting database backup...
echo Backup file: %BACKUP_FILE%

pg_dump -h localhost -U projectalpha_user -d projectalpha -F c -f "%BACKUP_FILE%"

IF %ERRORLEVEL% EQU 0 (
    echo Backup completed successfully.
    echo Saved to: %BACKUP_FILE%
) ELSE (
    echo Backup failed with error code: %ERRORLEVEL%
)

REM Keep only last 7 backups
forfiles /p "%BACKUP_DIR%" /m "projectalpha_*.sql" /d -7 /c "cmd /c del @path" 2>nul

SET PGPASSWORD=
