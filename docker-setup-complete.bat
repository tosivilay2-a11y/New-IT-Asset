@echo off
echo ============================================================
echo Asset Management System - Complete Docker Setup
echo ============================================================
echo.
echo This script will:
echo 1. Build all Docker images (Backend, Frontend, Database)
echo 2. Start all services
echo 3. Initialize database
echo 4. Seed sample data
echo.
pause

:: Check Docker
echo [1/7] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)
echo [OK] Docker is running

:: Clean up old containers
echo.
echo [2/7] Cleaning up old containers...
docker-compose down -v
echo [OK] Cleanup complete

:: Build images
echo.
echo [3/7] Building Docker images...
echo This may take 5-10 minutes on first run...
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)
echo [OK] Images built successfully

:: Start services
echo.
echo [4/7] Starting services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)
echo [OK] Services started

:: Wait for database
echo.
echo [5/7] Waiting for database to be ready (20 seconds)...
timeout /t 20 /nobreak >nul
echo [OK] Database should be ready

:: Initialize database
echo.
echo [6/7] Initializing database...
docker-compose exec -T backend alembic upgrade head
if %errorlevel% neq 0 (
    echo [WARNING] Migration failed. Retrying in 10 seconds...
    timeout /t 10 /nobreak >nul
    docker-compose exec -T backend alembic upgrade head
)
echo [OK] Database initialized

:: Seed data
echo.
echo [7/7] Seeding sample data...
docker-compose exec -T backend python seed_data.py
if %errorlevel% neq 0 (
    echo [WARNING] Seeding failed. You can run it manually later.
) else (
    echo [OK] Sample data created
)

:: Show status
echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Services Status:
docker-compose ps
echo.
echo ============================================================
echo Access the application:
echo ============================================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Database:  localhost:5432
echo.
echo ============================================================
echo Default Login:
echo ============================================================
echo.
echo Email:    admin@example.com
echo Password: admin123
echo.
echo ============================================================
echo Useful Commands:
echo ============================================================
echo.
echo View logs:     docker-compose logs -f
echo Stop all:      docker-compose down
echo Restart:       docker-compose restart
echo Rebuild:       docker-compose build --no-cache
echo.
echo ============================================================

:: Open browser
set /p OPEN="Open application in browser? (Y/N): "
if /i "%OPEN%"=="Y" (
    timeout /t 2 /nobreak >nul
    start http://localhost:3000
)

echo.
pause
