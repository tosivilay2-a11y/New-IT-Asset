@echo off
echo ================================================
echo Backup assetdb Database
echo ================================================
echo.

set BACKUP_FILE=assetdb_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql
set BACKUP_FILE=%BACKUP_FILE: =0%

echo Creating backup: %BACKUP_FILE%
echo.

docker exec -it asset-db pg_dump -U postgres assetdb > %BACKUP_FILE%

if errorlevel 1 (
    echo.
    echo ERROR: Backup failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo Backup completed successfully!
echo ================================================
echo.
echo Backup file: %BACKUP_FILE%
echo.
echo To restore this backup to it_asset_db:
echo   docker exec -i asset-db psql -U postgres it_asset_db ^< %BACKUP_FILE%
echo.
echo ================================================
pause
