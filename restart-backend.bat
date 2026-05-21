@echo off
echo ========================================
echo Restarting Backend Server
echo ========================================
echo.

echo This will:
echo   1. Stop any running backend process
echo   2. Start backend with new routes loaded
echo.

echo Step 1: Stopping any existing backend on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found process: %%a
    taskkill /PID %%a /F >nul 2>&1
    echo ✅ Stopped process %%a
)
echo.

echo Step 2: Starting backend server...
echo.
cd backend
call venv\Scripts\activate
echo Starting uvicorn on http://localhost:8000...
echo.
echo ⚠️  Keep this window open!
echo ⚠️  Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --port 8000
