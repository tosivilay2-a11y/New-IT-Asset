@echo off
echo ========================================
echo Applying Database to PostgreSQL
echo ========================================
echo.

echo Checking PostgreSQL connection...
echo.

REM Test if psql is available
where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL command line tools not found in PATH.
    echo.
    echo Please install PostgreSQL or add it to your PATH.
    echo Download from: https://www.postgresql.org/download/windows/
    echo.
    echo Alternatively, use Docker:
    echo   docker-compose up -d db
    echo.
    pause
    exit /b 1
)

echo PostgreSQL tools found!
echo.

REM Set PostgreSQL connection details
set PGHOST=localhost
set PGPORT=5432
set PGUSER=postgres
set PGPASSWORD=postgres

echo Connecting to PostgreSQL at %PGHOST%:%PGPORT%
echo.

REM Create database
echo Step 1: Creating database 'it_asset_db'...
psql -h %PGHOST% -p %PGPORT% -U %PGUSER% -c "CREATE DATABASE it_asset_db;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Database created successfully
) else (
    echo ⚠ Database may already exist (continuing...)
)
echo.

REM Apply schema
echo Step 2: Creating tables (this may take a minute)...
psql -h %PGHOST% -p %PGPORT% -U %PGUSER% -d it_asset_db -f backend\scripts\schema-postgres.sql
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Error creating tables
    echo.
    echo Please check:
    echo   1. PostgreSQL is running on port 5432
    echo   2. Username: postgres, Password: postgres
    echo   3. File exists: backend\scripts\schema-postgres.sql
    echo.
    pause
    exit /b 1
)
echo ✓ Tables created successfully
echo.

REM Verify tables
echo Step 3: Verifying tables...
psql -h %PGHOST% -p %PGPORT% -U %PGUSER% -d it_asset_db -c "SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';"
echo.

echo ========================================
echo ✓ Database Applied Successfully!
echo ========================================
echo.
echo Database: it_asset_db
echo Host: localhost:5432
echo.
echo Next steps:
echo   1. cd backend
echo   2. npm install
echo   3. npm run db:seed
echo   4. npm run dev
echo.
echo ========================================
pause
