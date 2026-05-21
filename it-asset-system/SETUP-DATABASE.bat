@echo off
cls
echo ========================================
echo IT Asset Management System
echo Database Setup
echo ========================================
echo.
echo This script will create the database and tables
echo for the IT Asset Management System.
echo.
echo Choose your PostgreSQL setup:
echo.
echo   1. Docker PostgreSQL (Recommended)
echo   2. Local PostgreSQL Installation
echo   3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto docker
if "%choice%"=="2" goto local
if "%choice%"=="3" goto end

echo Invalid choice. Please try again.
pause
goto start

:docker
echo.
echo ========================================
echo Using Docker PostgreSQL
echo ========================================
call apply-database-docker.bat
goto end

:local
echo.
echo ========================================
echo Using Local PostgreSQL
echo ========================================
call apply-database.bat
goto end

:end
echo.
echo Setup script finished.
