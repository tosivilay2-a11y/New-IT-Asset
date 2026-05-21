@echo off
echo ========================================
echo FIX DATABASE AND START BACKEND
echo ========================================
echo.
echo This will:
echo   1. Fix database schema
echo   2. Seed all data
echo   3. Start backend
echo.
echo Press Ctrl+C to cancel, or
pause
echo.

cd backend
call venv\Scripts\activate

echo ========================================
echo Step 1: Fixing Database Schema
echo ========================================
echo.
python recreate_tables.py --yes
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to recreate tables!
    echo Check if PostgreSQL is running.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Seeding Data
echo ========================================
echo.

echo Seeding location hierarchy...
python seed_location_hierarchy.py
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Location hierarchy seed failed
)

echo.
echo Seeding asset control data...
python seed_asset_control_data.py
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Asset control data seed failed
)

echo.
echo Creating test user...
python create_test_user.py
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Test user creation failed
)

echo.
echo ========================================
echo Step 3: Starting Backend
echo ========================================
echo.
echo Backend starting on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --port 8000
