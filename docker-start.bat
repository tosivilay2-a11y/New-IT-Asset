@echo off
echo ============================================================
echo Asset Management System - Docker Setup
echo ============================================================
echo.

:: Check if Docker is installed
echo [1/6] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not running
    echo.
    echo Please install Docker Desktop:
    echo 1. Download from: https://www.docker.com/products/docker-desktop/
    echo 2. Install and restart your computer
    echo 3. Start Docker Desktop
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)
echo [OK] Docker is installed

:: Check if Docker is running
echo.
echo [2/6] Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running
    echo.
    echo Please start Docker Desktop:
    echo 1. Open Docker Desktop from Start Menu
    echo 2. Wait for the whale icon to be steady in system tray
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)
echo [OK] Docker is running

:: Check if docker-compose.yml exists
if not exist docker-compose.yml (
    echo [ERROR] docker-compose.yml not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

:: Stop any existing containers
echo.
echo [3/6] Stopping any existing containers...
docker-compose down >nul 2>&1
echo [OK] Cleaned up existing containers

:: Start services
echo.
echo [4/6] Starting services (this may take a few minutes on first run)...
echo.
echo Downloading images and starting containers...
docker-compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    echo.
    echo Try these steps:
    echo 1. Make sure Docker Desktop is running
    echo 2. Check if ports 3000, 8000, 5432 are available
    echo 3. Run: docker-compose logs
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Services started successfully

:: Wait for database to be ready
echo.
echo [5/6] Waiting for database to be ready (15 seconds)...
timeout /t 15 /nobreak >nul
echo [OK] Database should be ready

:: Initialize database
echo.
echo [6/6] Initializing database...
echo.

echo Creating database tables...
docker-compose exec -T backend alembic upgrade head
if %errorlevel% neq 0 (
    echo [WARNING] Failed to create tables
    echo The database might need more time to start
    echo.
    echo Try running manually:
    echo   docker-compose exec backend alembic upgrade head
    echo   docker-compose exec backend python seed_data.py
    echo.
) else (
    echo [OK] Tables created
    
    echo.
    echo Seeding sample data...
    docker-compose exec -T backend python seed_data.py
    if %errorlevel% neq 0 (
        echo [WARNING] Failed to seed data
        echo You can run this manually later:
        echo   docker-compose exec backend python seed_data.py
    ) else (
        echo [OK] Sample data created
    )
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
echo Application URLs:
echo ============================================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo ============================================================
echo Default Login Credentials:
echo ============================================================
echo.
echo Email:    admin@example.com
echo Password: admin123
echo.
echo ============================================================
echo Useful Commands:
echo ============================================================
echo.
echo View logs:           docker-compose logs -f
echo Stop services:       docker-compose down
echo Restart services:    docker-compose restart
echo View status:         docker-compose ps
echo.
echo ============================================================

:: Ask to open browser
echo.
set /p OPEN_BROWSER="Open application in browser? (Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    echo.
    echo Opening application...
    timeout /t 2 /nobreak >nul
    start http://localhost:3000
)

echo.
echo Press any key to exit...
pause >nul
