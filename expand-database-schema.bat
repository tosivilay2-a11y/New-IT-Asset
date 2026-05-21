@echo off
echo ================================================
echo Expand Database Schema
echo ================================================
echo.
echo This will add 20+ new tables to your database:
echo   - Countries, Provinces, Companies, Departments
echo   - UserTypes, Roles, Permissions
echo   - MainCategories, AssetStatuses
echo   - AssetSequences, AssetAssignments, AssetEvents
echo   - StockCountSessions, Reconciliations
echo   - ApprovalLevels, Approvals
echo   - BudgetPlans
echo   - AuditLogs, Notifications
echo.
echo Your existing data will NOT be affected.
echo.
pause

echo.
echo Running schema expansion...
docker-compose exec backend python expand_schema.py

if errorlevel 1 (
    echo.
    echo ERROR: Schema expansion failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo Schema Expansion Complete!
echo ================================================
echo.
echo Verifying tables...
docker exec -it asset-db psql -U postgres -d assetdb -c "\dt" | findstr "countries\|provinces\|companies\|departments\|usertypes\|userroles\|permissions"

echo.
echo Your database now has the comprehensive schema!
echo.
echo Next steps:
echo   1. Seed initial data (countries, companies, etc.)
echo   2. Update your backend models
echo   3. Test the new features
echo.
echo ================================================
pause
