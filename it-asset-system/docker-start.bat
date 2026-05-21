@echo off
echo ================================================
echo Starting IT Asset Management System
echo ================================================
echo.

cd /d "%~dp0"

echo Building and starting containers...
docker-compose up -d --build

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ================================================
echo Services Status:
echo ================================================
docker-compose ps

echo.
echo ================================================
echo IT Asset Management System is starting!
echo ================================================
echo.
echo Backend API: http://localhost:5000
echo Health Check: http://localhost:5000/health
echo.
echo Database: PostgreSQL on port 5433
echo   - Database: it_asset_db
echo   - User: postgres
echo   - Password: postgres
echo.
echo Default Users:
echo   Admin:   admin@example.com / admin123
echo   Manager: manager@example.com / manager123
echo   User:    user@example.com / user123
echo.
echo View logs: docker-compose logs -f
echo Stop: docker-compose down
echo ================================================
pause
