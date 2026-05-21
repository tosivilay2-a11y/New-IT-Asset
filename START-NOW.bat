@echo off
echo ============================================================
echo Starting Asset Management System
echo ============================================================
echo.

echo Stopping any existing containers...
docker-compose down 2>nul

echo.
echo Starting services (this may take a few minutes first time)...
docker-compose up -d

echo.
echo Waiting for services to start (20 seconds)...
timeout /t 20 /nobreak >nul

echo.
echo Initializing database...
docker-compose exec -T backend alembic upgrade head 2>nul
if %errorlevel% neq 0 (
    echo Waiting 10 more seconds for database...
    timeout /t 10 /nobreak >nul
    docker-compose exec -T backend alembic upgrade head
)

echo.
echo Seeding sample data...
docker-compose exec -T backend python seed_data.py

echo.
echo ============================================================
echo Application Started!
echo ============================================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Login:
echo Email:    admin@example.com
echo Password: admin123
echo.
echo ============================================================
echo.

start http://localhost:3000

pause
