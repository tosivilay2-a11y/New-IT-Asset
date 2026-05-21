@echo off
echo ================================================
echo Restarting IT Asset Management System
echo ================================================
echo.

cd /d "%~dp0"

echo Stopping containers...
docker-compose down

echo.
echo Starting containers...
docker-compose up -d

echo.
echo ================================================
echo Services restarted!
echo ================================================
echo.
echo View logs: docker-compose logs -f
echo ================================================
pause
