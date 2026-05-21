@echo off
echo ========================================
echo Admin System Configuration Setup
echo ========================================
echo.

echo Step 1: Verifying database tables...
cd backend
call venv\Scripts\activate
python verify_tables.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Creating missing tables...
    python create_location_tables.py
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create tables
        pause
        exit /b 1
    )
)
echo.

echo Step 2: Checking if data exists...
python -c "from app.core.database import SessionLocal; from app.models.country import Country; db = SessionLocal(); count = db.query(Country).count(); db.close(); exit(0 if count > 0 else 1)"
if %ERRORLEVEL% NEQ 0 (
    echo No data found. Seeding location hierarchy...
    python seed_location_hierarchy.py
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to seed data
        pause
        exit /b 1
    )
) else (
    echo Data already exists, skipping seed.
)
echo.

echo Step 3: Final verification...
python verify_tables.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Admin pages are ready at:
echo   http://localhost:3000/admin/config
echo.
echo API documentation:
echo   http://localhost:8000/docs
echo.
echo Available routes:
echo   - /countries
echo   - /provinces
echo   - /companies
echo   - /main-categories
echo   - /asset-utils/preview-asset-id
echo   - /asset-utils/generate-qr-code
echo.
echo Make sure backend is running:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload --port 8000
echo.
pause
