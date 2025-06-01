@echo off
echo Starting TRINETRA System...

:: Start MongoDB (if installed locally)
echo Starting MongoDB...
start "MongoDB" mongod

:: Initialize the database
echo Initializing database...
python backend/database/init_db.py

:: Start the FastAPI backend
echo Starting backend server...
start "TRINETRA Backend" uvicorn backend.api.main:app --reload --port 8000

:: Start the Streamlit frontend
echo Starting frontend...
start "TRINETRA Frontend" streamlit run frontend/dashboard.py

echo TRINETRA system is running!
echo Backend API: http://localhost:8000
echo Frontend Dashboard: http://localhost:8501
echo.
echo Press any key to stop all services...
pause

:: Cleanup
taskkill /F /IM uvicorn.exe
taskkill /F /IM streamlit.exe
taskkill /F /IM mongod.exe
