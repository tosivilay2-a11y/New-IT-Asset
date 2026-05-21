@echo off
echo ========================================
echo Asset Management System - Quick Start
echo ========================================
echo.

echo Step 1: Checking if Docker is running...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not running
    echo Please install Docker Desktop or run services manually
    pause
    exit /b 1
)

echo Step 2: Starting services with Docker Compose...
docker-compose up -d

echo.
echo Step 3: Waiting for services to start (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo Step 4: Running database migrations...
docker-compose exec -T backend alembic upgrade head

echo.
echo Step 5: Seeding sample data...
docker-compose exec -T backend python seed_data.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Services are running:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
echo Default Login Credentials:
echo - Admin: admin@example.com / admin123
echo - Staff: staff@example.com / staff123
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:3000

echo.
echo To view logs: docker-compose logs -f
echo To stop services: docker-compose down
echo.
pause
