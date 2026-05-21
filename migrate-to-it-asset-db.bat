@echo off
echo ================================================
echo Migrating to it_asset_db Database
echo ================================================
echo.
echo This will:
echo   1. Stop current containers
echo   2. Create it_asset_db database
echo   3. Restart with new database
echo.
echo WARNING: This will create a fresh database.
echo If you want to keep data from assetdb, backup first!
echo.
pause

echo.
echo Step 1: Stopping containers...
docker-compose down

echo.
echo Step 2: Creating it_asset_db database...
docker-compose up -d db

echo Waiting for database to be ready...
timeout /t 5 /nobreak >nul

echo Creating it_asset_db if it doesn't exist...
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;" 2>nul

echo.
echo Step 3: Running database migrations...
docker-compose up -d backend

echo Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

echo.
echo Step 4: Starting frontend...
docker-compose up -d frontend

echo.
echo ================================================
echo Migration Complete!
echo ================================================
echo.
echo Checking services...
docker-compose ps

echo.
echo Access your application:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Default users:
echo   admin@example.com / admin123
echo   staff@example.com / staff123
echo.
echo ================================================
pause
