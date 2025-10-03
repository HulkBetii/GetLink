@echo off
REM Windows Build Script for Course Link Getter
REM Simple batch file to run the Python build script

echo ========================================
echo Course Link Getter - Windows Builder
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found, starting build...
echo.

REM Run the build script
python build_windows.py

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Files created in 'release' folder:
dir /b release\*.exe 2>nul
echo.
echo To test the application:
echo   powershell -ExecutionPolicy Bypass -File smoketest.ps1
echo.
pause
