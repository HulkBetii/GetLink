@echo off
REM Build script for Windows
echo 🪟 Building Course Link Getter for Windows...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Create Windows executable
pyinstaller ^
    --name="Course Link Getter" ^
    --windowed ^
    --onedir ^
    --icon=course_link_getter/assets/icon.ico ^
    --add-data="course_link_getter/assets;courses_link_getter/assets" ^
    --add-data="course_link_getter/core;courses_link_getter/core" ^
    --add-data="course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5" ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=PyQt5.sip ^
    --clean ^
    course_link_getter/launch_pyqt5.py

REM Check if build was successful
if exist "dist\Course Link Getter" (
    echo ✅ Windows executable created successfully!
    echo 📁 App location: dist\Course Link Getter\
    
    REM Create ZIP archive
    echo 📦 Creating ZIP archive...
    powershell Compress-Archive -Path "dist\Course Link Getter\*" -DestinationPath "Course_Link_Getter_Windows.zip" -Force
    echo ✅ ZIP created: Course_Link_Getter_Windows.zip
) else (
    echo ❌ Build failed!
    exit /b 1
)

echo 🎉 Windows build completed!
pause
