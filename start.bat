@echo off
REM Quick start script for Windows

echo.
echo ================================
echo TERRIBLE Web Application Example
echo ================================
echo.
echo WARNING: This is intentionally bad code!
echo Do NOT use these patterns in real projects!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
echo.

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo.

REM Remove old database if exists
if exist students.db (
    echo Removing old database...
    del students.db
)

echo Starting the server...
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python terrible_server.py
pause

