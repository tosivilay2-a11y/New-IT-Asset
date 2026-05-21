@echo off
echo ============================================================
echo Reset Asset Management System
echo ============================================================
echo.
echo WARNING: This will delete all data including:
echo - Database data
echo - User accounts
echo - Assets, inventory, and audit records
echo.
set /p CONFIRM="Are you sure you want to reset everything? (yes/no): "

if /i not "%CONFIRM%"=="yes" (
    echo.
    echo Reset cancelled
    pause
    exit /b 0
)

echo.
echo [1/3] Stopping and removing all containers and volumes...
docker-compose down -v

if %errorlevel% neq 0 (
    echo [ERROR] Failed to remove containers
    pause
    exit /b 1
)
echo [OK] Containers and volumes removed

echo.
echo [2/3] Starting fresh services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)
echo [OK] Services started

echo.
echo [3/3] Waiting for database and initializing...
timeout /t 15 /nobreak >nul

docker-compose exec -T backend alembic upgrade head
docker-compose exec -T backend python seed_data.py

echo.
echo ============================================================
echo Reset Complete!
echo ============================================================
echo.
echo The application has been reset to initial state.
echo.
echo Login with:
echo Email:    admin@example.com
echo Password: admin123
echo.
echo Application: http://localhost:3000
echo.
pause
