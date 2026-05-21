@echo off
echo ============================================================
echo Starting Backend and Database with Docker
echo ============================================================
echo.
echo This will start:
echo - PostgreSQL Database (port 5432)
echo - Backend API (port 8000)
echo.
echo Frontend will run separately with: npm start
echo.
pause

:: Check Docker
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

:: Start services
echo.
echo Starting services...
docker-compose -f docker-compose-backend-only.yml up -d --build

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

:: Wait for database
echo.
echo Waiting for database (15 seconds)...
timeout /t 15 /nobreak >nul

:: Initialize database
echo.
echo Initializing database...
docker-compose -f docker-compose-backend-only.yml exec -T backend alembic upgrade head

:: Seed data
echo.
echo Seeding sample data...
docker-compose -f docker-compose-backend-only.yml exec -T backend python seed_data.py

:: Show status
echo.
echo ============================================================
echo Backend and Database Started!
echo ============================================================
echo.
docker-compose -f docker-compose-backend-only.yml ps
echo.
echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Database:    localhost:5432
echo.
echo ============================================================
echo Next Steps:
echo ============================================================
echo.
echo 1. Open a new terminal
echo 2. Navigate to frontend folder: cd frontend
echo 3. Install dependencies (first time): npm install
echo 4. Start frontend: npm start
echo 5. Access application: http://localhost:3000
echo.
echo Login with:
echo Email:    admin@example.com
echo Password: admin123
echo.
echo ============================================================
echo.
echo To stop: docker-compose -f docker-compose-backend-only.yml down
echo.
pause
