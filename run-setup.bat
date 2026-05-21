@echo off
cd backend
call venv\Scripts\activate.bat
python create_location_tables.py
python seed_location_hierarchy.py
pause
