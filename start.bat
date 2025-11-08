@echo off
echo ============================================
echo Stock Price Prediction and Sentiment Analysis
echo ============================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Starting Flask server...
echo.
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

