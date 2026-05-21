@echo off
echo ================================================
echo IT Asset Management System - Logs
echo ================================================
echo.
echo Press Ctrl+C to exit
echo.

cd /d "%~dp0"

docker-compose logs -f
