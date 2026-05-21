@echo off
echo ================================================
echo Creating it_asset_db Database in Docker PostgreSQL
echo ================================================
echo.

echo Checking if PostgreSQL container is running...
docker ps | findstr asset-db >nul
if errorlevel 1 (
    echo ERROR: PostgreSQL container 'asset-db' is not running
    echo Please start it first with: docker-compose up -d
    pause
    exit /b 1
)

echo.
echo Creating database it_asset_db...
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"

if errorlevel 1 (
    echo.
    echo Note: If you see "already exists" error, the database is already created.
    echo This is OK - you can proceed with the setup.
) else (
    echo.
    echo SUCCESS: Database created!
)

echo.
echo Verifying database...
docker exec -it asset-db psql -U postgres -c "\l" | findstr it_asset_db

echo.
echo ================================================
echo Next step: Run setup-complete.bat in backend folder
echo ================================================
pause
