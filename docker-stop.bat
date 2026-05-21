@echo off
echo ============================================================
echo Stopping Asset Management System
echo ============================================================
echo.

docker-compose down

if %errorlevel% equ 0 (
    echo.
    echo [OK] All services stopped successfully
    echo.
    echo To start again, run: docker-start.bat
) else (
    echo.
    echo [ERROR] Failed to stop services
    echo.
    echo Try manually:
    echo   docker-compose down
)

echo.
pause
