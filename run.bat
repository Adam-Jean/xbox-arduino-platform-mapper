@echo off
echo Platform Controller Launcher
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Please ensure Python 3.7+ is installed and in PATH
        pause
        exit /b 1
    )
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo Setup complete!
    echo.
) else (
    call venv\Scripts\activate.bat
)

echo Starting Platform Controller...
echo.
python main.py
pause
