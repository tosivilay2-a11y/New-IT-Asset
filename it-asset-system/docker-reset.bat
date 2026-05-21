@echo off
echo ================================================
echo RESET IT Asset Management System
echo ================================================
echo.
echo WARNING: This will delete all data!
echo.
pause

cd /d "%~dp0"

echo Stopping and removing containers...
docker-compose down -v

echo.
echo Removing images...
docker-compose down --rmi local

echo.
echo Starting fresh...
docker-compose up -d --build

echo.
echo ================================================
echo System reset complete!
echo ================================================
echo.
echo The database has been recreated with fresh data.
echo Default users are available again.
echo ================================================
pause
