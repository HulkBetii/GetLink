@echo off
REM Comprehensive Windows Issues Fix Script
REM Handles Python installation, PATH issues, and build problems

title Course Link Getter - Windows Issues Fixer
color 0B

echo.
echo ========================================
echo   Course Link Getter - Issues Fixer
echo ========================================
echo.

echo This script will help fix common Windows build issues:
echo 1. Python not found
echo 2. Python not in PATH
echo 3. Build tools missing
echo 4. Permission issues
echo.

pause

:MAIN_MENU
cls
echo.
echo ========================================
echo   Course Link Getter - Issues Fixer
echo ========================================
echo.
echo Choose an option:
echo.
echo 1. Check Python installation
echo 2. Install Python automatically
echo 3. Fix Python PATH issues
echo 4. Install build tools (NSIS, UPX)
echo 5. Run build with fixes
echo 6. Test build system
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto CHECK_PYTHON
if "%choice%"=="2" goto INSTALL_PYTHON
if "%choice%"=="3" goto FIX_PATH
if "%choice%"=="4" goto INSTALL_TOOLS
if "%choice%"=="5" goto RUN_BUILD
if "%choice%"=="6" goto TEST_BUILD
if "%choice%"=="7" goto EXIT
goto MAIN_MENU

:CHECK_PYTHON
cls
echo.
echo ========================================
echo   Checking Python Installation
echo ========================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo.
    echo Checking common Python installation locations...
    
    if exist "C:\Python312\python.exe" (
        echo ✅ Found Python at: C:\Python312\python.exe
        set PYTHON_PATH=C:\Python312
    ) else if exist "C:\Python311\python.exe" (
        echo ✅ Found Python at: C:\Python311\python.exe
        set PYTHON_PATH=C:\Python311
    ) else if exist "C:\Python310\python.exe" (
        echo ✅ Found Python at: C:\Python310\python.exe
        set PYTHON_PATH=C:\Python310
    ) else if exist "C:\Python39\python.exe" (
        echo ✅ Found Python at: C:\Python39\python.exe
        set PYTHON_PATH=C:\Python39
    ) else if exist "C:\Python38\python.exe" (
        echo ✅ Found Python at: C:\Python38\python.exe
        set PYTHON_PATH=C:\Python38
    ) else (
        echo ❌ Python not found in common locations
        echo.
        echo Please install Python from: https://python.org
        echo Or use option 2 to install automatically
    )
) else (
    echo ✅ Python found in PATH
    python --version
)

echo.
pause
goto MAIN_MENU

:INSTALL_PYTHON
cls
echo.
echo ========================================
echo   Installing Python
echo ========================================
echo.

echo Choose installation method:
echo 1. Automatic download and install
echo 2. PowerShell script (recommended)
echo 3. Back to main menu
echo.
set /p install_choice="Enter your choice (1-3): "

if "%install_choice%"=="1" (
    call install_python_windows.bat
) else if "%install_choice%"=="2" (
    echo Running PowerShell installer...
    powershell -ExecutionPolicy Bypass -File install_python_windows.ps1
) else if "%install_choice%"=="3" (
    goto MAIN_MENU
) else (
    goto INSTALL_PYTHON
)

echo.
pause
goto MAIN_MENU

:FIX_PATH
cls
echo.
echo ========================================
echo   Fixing Python PATH Issues
echo ========================================
echo.

echo This will help you add Python to your PATH environment variable.
echo.

REM Check if we found Python in common locations
if defined PYTHON_PATH (
    echo Found Python at: %PYTHON_PATH%
    echo.
    echo Adding to PATH for current session...
    set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%
    echo.
    echo Testing Python...
    python --version
    if not errorlevel 1 (
        echo ✅ Python is now accessible!
        echo.
        echo To make this permanent, you need to add to system PATH:
        echo 1. Open System Properties
        echo 2. Go to Advanced tab
        echo 3. Click Environment Variables
        echo 4. Edit PATH variable
        echo 5. Add: %PYTHON_PATH%
        echo 6. Add: %PYTHON_PATH%\Scripts
    )
) else (
    echo No Python installation found.
    echo Please install Python first using option 2.
)

echo.
pause
goto MAIN_MENU

:INSTALL_TOOLS
cls
echo.
echo ========================================
echo   Installing Build Tools
echo ========================================
echo.

echo This will download and install required build tools:
echo - NSIS (for creating Windows installer)
echo - UPX (for compressing executables)
echo.

set /p install_tools="Continue? (Y/N): "
if /i not "%install_tools%"=="Y" goto MAIN_MENU

echo.
echo The build script will automatically download these tools.
echo You can also download manually:
echo - NSIS: https://nsis.sourceforge.io/
echo - UPX: https://upx.github.io/
echo.

echo Running build script to download tools...
python build_windows.py --download-tools-only

echo.
pause
goto MAIN_MENU

:RUN_BUILD
cls
echo.
echo ========================================
echo   Running Build with Fixes
echo ========================================
echo.

echo This will run the build script with automatic fixes.
echo.

REM Ensure Python is in PATH
if defined PYTHON_PATH (
    set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%
)

echo Starting build process...
call build_windows.bat

echo.
pause
goto MAIN_MENU

:TEST_BUILD
cls
echo.
echo ========================================
echo   Testing Build System
echo ========================================
echo.

echo Running comprehensive tests...
echo.

REM Test Python
echo 1. Testing Python...
python --version
if errorlevel 1 (
    echo ❌ Python test failed
) else (
    echo ✅ Python test passed
)

echo.
echo 2. Testing pip...
pip --version
if errorlevel 1 (
    echo ❌ pip test failed
) else (
    echo ✅ pip test passed
)

echo.
echo 3. Testing PyInstaller...
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller test failed
) else (
    echo ✅ PyInstaller test passed
)

echo.
echo 4. Testing project structure...
if exist "course_link_getter\launch_pyqt5.py" (
    echo ✅ Project structure test passed
) else (
    echo ❌ Project structure test failed
)

echo.
echo 5. Running PowerShell test script...
if exist "test_windows_build.ps1" (
    powershell -ExecutionPolicy Bypass -File test_windows_build.ps1 -SkipInstaller
) else (
    echo ❌ Test script not found
)

echo.
pause
goto MAIN_MENU

:EXIT
cls
echo.
echo ========================================
echo   Thank you for using Issues Fixer!
echo ========================================
echo.
echo If you still have problems:
echo 1. Check the README_BUILD.md file
echo 2. Make sure you have Windows 10/11 x64
echo 3. Try running as administrator
echo 4. Check Windows Defender settings
echo.
echo Good luck with your build!
echo.
pause
exit /b 0
