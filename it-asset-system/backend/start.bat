@echo off
echo ================================================
echo IT Asset Management - Starting Server
echo ================================================
echo.

cd /d "%~dp0"

echo Starting development server...
echo Press Ctrl+C to stop the server
echo.

call npm run dev
