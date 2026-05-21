@echo off
echo ================================================
echo Initialize it_asset_db Database
echo ================================================
echo.

echo Step 1: Stopping backend to prevent conflicts...
docker-compose stop backend

echo.
echo Step 2: Creating it_asset_db database...
docker exec -it asset-db psql -U postgres -c "DROP DATABASE IF EXISTS it_asset_db;"
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"

echo.
echo Step 3: Creating tables...
docker-compose run --rm backend python -c "from app.models import *; from app.core.database import engine, Base; Base.metadata.create_all(bind=engine); print('Tables created successfully!')"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create tables
    pause
    exit /b 1
)

echo.
echo Step 4: Seeding initial data...
docker-compose run --rm backend python backend/seed_data.py

echo.
echo Step 5: Starting backend...
docker-compose up -d backend

echo.
echo Waiting for backend to start...
timeout /t 10 /nobreak >nul

echo.
echo ================================================
echo Initialization Complete!
echo ================================================
echo.
echo Checking services...
docker-compose ps

echo.
echo Test the backend:
echo   curl http://localhost:8000/
echo   start http://localhost:8000/docs
echo.
echo ================================================
pause
