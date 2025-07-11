@echo off
echo ============================================
echo    Fliqlo Timer - Installation Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

echo.
echo [INFO] Installing pygame for button sounds...
pip install pygame

if %errorlevel% neq 0 (
    echo [WARNING] Could not install pygame
    echo [INFO] Buttons will work without sound
)

echo.
echo [INFO] Creating data directory...
if not exist "data" mkdir data

echo.
echo [INFO] Checking sfx directory...
if not exist "sfx" mkdir sfx

if not exist "sfx\button_1.mp3" (
    echo [WARNING] Sound file 'sfx\button_1.mp3' not found
    echo [INFO] Add 'button_1.mp3' to 'sfx\' folder for button sounds
)

if not exist "sfx\whitenoise_1.mp3" (
    echo [WARNING] Background music 'sfx\whitenoise_1.mp3' not found
    echo [INFO] Add 'whitenoise_1.mp3' to 'sfx\' folder for background music
    echo [INFO] App will work without background music
)

echo.
echo [SUCCESS] Setup completed!
echo.
echo To run the app:
echo 1. Double-click 'run.bat'
echo 2. Or run 'python main.py' from this directory
echo.
pause
