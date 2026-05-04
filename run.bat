@echo off
REM Placement Prep Application - Run Script for Windows

echo ==========================================
echo Placement Prep Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Using Python:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Check if database exists
if not exist "placement_prep.db" (
    echo Database not found. Initializing...
    python init_db.py
    echo.
)

REM Run test
echo Running setup tests...
python test_setup.py
echo.

REM Start application
echo Starting Flask application...
echo ==========================================
echo Open your browser and go to:
echo http://127.0.0.1:5000
echo ==========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
