@echo off
echo ================================================
echo Copy assetdb to it_asset_db
echo ================================================
echo.
echo This will:
echo   1. Create it_asset_db database
echo   2. Copy all data from assetdb to it_asset_db
echo.
pause

echo.
echo Step 1: Stopping backend...
docker-compose stop backend

echo.
echo Step 2: Creating it_asset_db...
docker exec -it asset-db psql -U postgres -c "DROP DATABASE IF EXISTS it_asset_db;"
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db WITH TEMPLATE assetdb OWNER postgres;"

if errorlevel 1 (
    echo.
    echo Template copy failed, trying dump/restore method...
    echo.
    docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
    docker exec -it asset-db pg_dump -U postgres assetdb | docker exec -i asset-db psql -U postgres it_asset_db
)

echo.
echo Step 3: Verifying copy...
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"

echo.
echo Step 4: Starting backend...
docker-compose up -d backend

echo.
echo Waiting for backend...
timeout /t 10 /nobreak >nul

echo.
echo ================================================
echo Copy Complete!
echo ================================================
echo.
echo Testing backend...
curl http://localhost:8000/

echo.
echo Services status:
docker-compose ps

echo.
echo Access your application:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo ================================================
pause
