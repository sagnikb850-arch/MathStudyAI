@echo off
REM Math Study AI - Windows Startup Script

echo.
echo ========================================
echo  Math Study AI - Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Create venv if it doesn't exist
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate venv
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [3/4] Installing dependencies...
pip install -r requirements.txt >nul 2>&1

REM Check for .env file
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and add your API key
    echo.
    echo Example:
    echo   - Copy: .env.example to .env
    echo   - Edit: .env and add OPENAI_API_KEY=sk-...
    echo.
    pause
)

REM Start backend
echo [4/4] Starting Math Study AI Backend...
echo.
echo Starting server on http://localhost:5000
echo Open frontend/index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py

pause
