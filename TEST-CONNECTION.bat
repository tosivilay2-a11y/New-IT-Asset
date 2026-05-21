@echo off
echo ======================================================================
echo TESTING BACKEND CONNECTION
echo ======================================================================
echo.

cd backend
call venv\Scripts\activate
python test_backend_simple.py

echo.
echo ======================================================================
echo.
echo If all tests passed, the backend is working correctly!
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Try logging in with:
echo   Email: admin@example.com
echo   Password: admin123
echo.
echo ======================================================================
pause
