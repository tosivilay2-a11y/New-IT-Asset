@echo off
echo ================================================
echo Restore assetdb to it_asset_db
echo ================================================
echo.

if "%~1"=="" (
    echo ERROR: Please provide backup file name
    echo.
    echo Usage: restore-to-it-asset-db.bat backup_file.sql
    echo.
    echo Available backups:
    dir /b assetdb_backup_*.sql 2>nul
    pause
    exit /b 1
)

set BACKUP_FILE=%~1

if not exist "%BACKUP_FILE%" (
    echo ERROR: Backup file not found: %BACKUP_FILE%
    pause
    exit /b 1
)

echo Restoring from: %BACKUP_FILE%
echo Target database: it_asset_db
echo.
pause

echo.
echo Creating it_asset_db if it doesn't exist...
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;" 2>nul

echo.
echo Restoring data...
docker exec -i asset-db psql -U postgres it_asset_db < "%BACKUP_FILE%"

if errorlevel 1 (
    echo.
    echo ERROR: Restore failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo Restore completed successfully!
echo ================================================
echo.
echo Database it_asset_db now contains data from %BACKUP_FILE%
echo.
echo Restart your application:
echo   docker-compose restart
echo.
echo ================================================
pause
