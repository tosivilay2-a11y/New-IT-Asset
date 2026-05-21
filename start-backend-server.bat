@echo off
echo Starting Backend Server...
cd /d D:\New-Asset-management\backend
call venv\Scripts\activate.bat
echo.
echo Backend server starting on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
