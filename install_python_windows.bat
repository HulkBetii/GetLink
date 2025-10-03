@echo off
REM Python Installation Script for Windows
REM Automatically downloads and installs Python if not found

title Course Link Getter - Python Installer
color 0A

echo.
echo ========================================
echo   Course Link Getter - Python Installer
echo ========================================
echo.

REM Check if Python is already installed
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python is already installed!
    python --version
    echo.
    echo You can now run: build_windows.bat
    pause
    exit /b 0
)

echo ❌ Python not found on this system.
echo.
echo This script will help you install Python automatically.
echo.

REM Check if we have internet connection
echo 🔍 Checking internet connection...
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo ❌ No internet connection found.
    echo Please connect to internet and try again.
    pause
    exit /b 1
)

echo ✅ Internet connection available.
echo.

REM Create temp directory
set TEMP_DIR=%TEMP%\CourseLinkGetter
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo 📥 Downloading Python installer...
echo.

REM Download Python installer (latest stable version)
set PYTHON_URL=https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe
set PYTHON_INSTALLER=%TEMP_DIR%\python-installer.exe

echo Downloading from: %PYTHON_URL%
echo Saving to: %PYTHON_INSTALLER%
echo.

REM Use PowerShell to download (more reliable than curl)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo ❌ Failed to download Python installer.
    echo Please download manually from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python installer downloaded successfully!
echo.

echo 🚀 Starting Python installation...
echo.
echo IMPORTANT: During installation, make sure to:
echo 1. ✅ Check "Add Python to PATH"
echo 2. ✅ Check "Install for all users" (if you have admin rights)
echo 3. ✅ Click "Install Now"
echo.

REM Run the installer
start /wait "" "%PYTHON_INSTALLER%"

echo.
echo 🔍 Verifying Python installation...

REM Wait a moment for PATH to update
timeout /t 3 /nobreak >nul

REM Check if Python is now available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python installation may have failed or PATH not updated.
    echo.
    echo Please try one of these solutions:
    echo 1. Restart Command Prompt and try again
    echo 2. Restart your computer
    echo 3. Manually add Python to PATH
    echo.
    echo Manual installation: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python installed successfully!
python --version
echo.

REM Clean up
if exist "%PYTHON_INSTALLER%" del "%PYTHON_INSTALLER%"
if exist "%TEMP_DIR%" rmdir "%TEMP_DIR%" 2>nul

echo 🎉 Python is ready!
echo.
echo You can now run: build_windows.bat
echo.
pause
