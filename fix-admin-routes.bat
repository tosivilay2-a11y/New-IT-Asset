@echo off
echo ========================================
echo Fix Admin Routes - Diagnostic and Repair
echo ========================================
echo.

echo Step 1: Checking if routes are registered...
cd backend
call venv\Scripts\activate
python check_routes.py
echo.

echo Step 2: Verifying database tables...
python verify_tables.py
echo.

echo Step 3: Testing if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Backend is running
    echo.
    echo Step 4: Testing admin endpoints...
    echo.
    echo Testing /countries:
    curl -s http://localhost:8000/countries
    echo.
    echo.
    echo Testing /main-categories:
    curl -s http://localhost:8000/main-categories
    echo.
) else (
    echo ❌ Backend is NOT running
    echo.
    echo Please start the backend server:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   uvicorn app.main:app --reload --port 8000
)

echo.
echo ========================================
echo Diagnostic Complete
echo ========================================
echo.
echo If routes are missing:
echo   1. Make sure backend server is restarted
echo   2. Check main.py has all route imports
echo   3. Check main.py has all include_router calls
echo.
echo To restart backend:
echo   1. Stop current backend (Ctrl+C)
echo   2. cd backend
echo   3. venv\Scripts\activate
echo   4. uvicorn app.main:app --reload --port 8000
echo.
pause
