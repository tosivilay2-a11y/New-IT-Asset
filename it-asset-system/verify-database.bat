@echo off
echo ================================================
echo Verifying PostgreSQL Database Setup
echo ================================================
echo.

echo Checking PostgreSQL container...
docker ps | findstr asset-db
if errorlevel 1 (
    echo ERROR: PostgreSQL container not running
    pause
    exit /b 1
)

echo.
echo Listing all databases...
docker exec -it asset-db psql -U postgres -c "\l"

echo.
echo Checking if it_asset_db exists...
docker exec -it asset-db psql -U postgres -c "\l" | findstr it_asset_db
if errorlevel 1 (
    echo.
    echo WARNING: it_asset_db database not found!
    echo Run create-database-docker.bat to create it.
) else (
    echo.
    echo SUCCESS: it_asset_db database exists!
    echo.
    echo Checking tables in it_asset_db...
    docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
)

echo.
echo ================================================
pause
