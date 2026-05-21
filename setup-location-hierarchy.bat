@echo off
echo ========================================
echo Location Hierarchy Setup
echo ========================================
echo.

echo Step 1: Creating database tables...
cd backend
call venv\Scripts\activate
python create_location_tables.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create tables
    pause
    exit /b 1
)
echo.

echo Step 2: Seeding location hierarchy data...
python seed_location_hierarchy.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to seed data
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo New API endpoints available:
echo   - http://localhost:8000/countries
echo   - http://localhost:8000/provinces
echo   - http://localhost:8000/companies
echo   - http://localhost:8000/main-categories
echo   - http://localhost:8000/asset-utils/preview-asset-id
echo   - http://localhost:8000/asset-utils/generate-qr-code
echo.
echo Please restart the backend server to use the new features.
echo.
pause
