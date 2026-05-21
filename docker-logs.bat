@echo off
echo ============================================================
echo Asset Management System - View Logs
echo ============================================================
echo.
echo Choose which logs to view:
echo.
echo 1. All services
echo 2. Backend only
echo 3. Frontend only
echo 4. Database only
echo 5. Follow all logs (real-time)
echo.
set /p CHOICE="Enter choice (1-5): "

echo.
echo Press Ctrl+C to stop viewing logs
echo.
timeout /t 2 /nobreak >nul

if "%CHOICE%"=="1" (
    docker-compose logs --tail=100
) else if "%CHOICE%"=="2" (
    docker-compose logs backend --tail=100
) else if "%CHOICE%"=="3" (
    docker-compose logs frontend --tail=100
) else if "%CHOICE%"=="4" (
    docker-compose logs db --tail=100
) else if "%CHOICE%"=="5" (
    docker-compose logs -f
) else (
    echo Invalid choice
    pause
    exit /b 1
)

echo.
pause
