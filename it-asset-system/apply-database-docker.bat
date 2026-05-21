@echo off
echo ========================================
echo Applying Database to Docker PostgreSQL
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Docker is not running or not installed
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo ✓ Docker is running
echo.

REM Find PostgreSQL container
echo Looking for PostgreSQL container...
for /f "tokens=*" %%i in ('docker ps --filter "ancestor=postgres" --format "{{.Names}}"') do set PG_CONTAINER=%%i

if "%PG_CONTAINER%"=="" (
    echo ✗ PostgreSQL container not found
    echo.
    echo Starting PostgreSQL with docker-compose...
    docker-compose up -d db
    timeout /t 5 /nobreak >nul
    
    REM Try to find container again
    for /f "tokens=*" %%i in ('docker ps --filter "ancestor=postgres" --format "{{.Names}}"') do set PG_CONTAINER=%%i
    
    if "%PG_CONTAINER%"=="" (
        echo ✗ Failed to start PostgreSQL
        echo.
        pause
        exit /b 1
    )
)

echo ✓ Found PostgreSQL container: %PG_CONTAINER%
echo.

REM Create database
echo Step 1: Creating database 'it_asset_db'...
docker exec %PG_CONTAINER% psql -U postgres -c "CREATE DATABASE it_asset_db;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Database created
) else (
    echo ⚠ Database may already exist (continuing...)
)
echo.

REM Apply schema
echo Step 2: Creating tables (this may take a minute)...
docker exec -i %PG_CONTAINER% psql -U postgres -d it_asset_db < backend\scripts\schema-postgres.sql
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Error creating tables
    pause
    exit /b 1
)
echo ✓ Tables created successfully
echo.

REM Verify tables
echo Step 3: Verifying tables...
docker exec %PG_CONTAINER% psql -U postgres -d it_asset_db -c "SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';"
echo.

REM List some tables
echo Sample tables created:
docker exec %PG_CONTAINER% psql -U postgres -d it_asset_db -c "\dt" | findstr "countries users assets"
echo.

echo ========================================
echo ✓ Database Applied Successfully!
echo ========================================
echo.
echo Container: %PG_CONTAINER%
echo Database: it_asset_db
echo Port: 5432
echo.
echo Next steps:
echo   1. cd backend
echo   2. npm install
echo   3. npm run db:seed
echo   4. npm run dev
echo.
echo ========================================
pause
