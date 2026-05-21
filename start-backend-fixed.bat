@echo off
echo Starting Backend Server with proper host binding...
echo Backend will be accessible on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

cd backend
call venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
