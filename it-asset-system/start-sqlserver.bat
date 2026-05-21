@echo off
echo ========================================
echo Starting SQL Server for IT Asset System
echo ========================================
echo.

REM Check if SQL Server container exists
docker ps -a --filter "name=it-asset-sqlserver" --format "{{.Names}}" > nul 2>&1

if errorlevel 1 (
    echo Creating new SQL Server container...
    docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" -p 1433:1433 --name it-asset-sqlserver -d mcr.microsoft.com/mssql/server:2019-latest
    echo.
    echo Waiting for SQL Server to start...
    timeout /t 10 /nobreak > nul
    echo.
) else (
    echo Starting existing SQL Server container...
    docker start it-asset-sqlserver
    echo.
    echo Waiting for SQL Server to be ready...
    timeout /t 5 /nobreak > nul
    echo.
)

echo ========================================
echo SQL Server is running!
echo ========================================
echo.
echo Connection Details:
echo   Server: localhost
echo   Port: 1433
echo   User: sa
echo   Password: YourStrong@Passw0rd
echo.
echo You can now run: npm run dev
echo ========================================
