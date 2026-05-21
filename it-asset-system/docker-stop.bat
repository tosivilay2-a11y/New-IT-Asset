@echo off
echo ================================================
echo Stopping IT Asset Management System
echo ================================================
echo.

cd /d "%~dp0"

docker-compose down

echo.
echo ================================================
echo Services stopped successfully!
echo ================================================
pause
