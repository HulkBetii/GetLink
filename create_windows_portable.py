#!/usr/bin/env python3
"""
Create portable executable that can run on Windows
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_portable_executable():
    """Create portable executable using PyInstaller"""
    print("🚀 Creating portable executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build command for portable executable
    cmd = [
        'pyinstaller',
        '--name=Course_Link_Getter_Portable',
        '--windowed',
        '--onefile',
        '--icon=course_link_getter/assets/icon.ico',
        '--add-data=course_link_getter/assets:courses_link_getter/assets',
        '--add-data=course_link_getter/core:courses_link_getter/core',
        '--add-data=course_link_getter/ui_pyqt5:courses_link_getter/ui_pyqt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.sip',
        '--clean',
        'course_link_getter/launch_pyqt5.py'
    ]
    
    print("📦 Building portable executable...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully")
        
        # Check if executable was created
        executable_path = "dist/Course_Link_Getter_Portable"
        if os.path.exists(executable_path):
            size_mb = os.path.getsize(executable_path) / (1024 * 1024)
            print(f"✅ Portable executable created: {executable_path}")
            print(f"📊 Size: {size_mb:.1f} MB")
            return executable_path
        else:
            print(f"❌ Executable not found: {executable_path}")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def create_windows_instructions():
    """Create instructions for Windows users"""
    instructions = """# 🪟 Course Link Getter - Windows Instructions

## 🚀 Quick Start

### Option 1: Use the Builder (Recommended)
1. **Download**: `Course_Link_Getter_Windows_Builder_FIXED.zip`
2. **Extract**: Unzip the file
3. **Run**: Double-click `BUILD_WINDOWS_EXE_FIXED.bat`
4. **Follow**: The on-screen instructions
5. **Get**: Your `Course_Link_Getter.exe` file

### Option 2: Manual Installation
If the builder doesn't work, follow these steps:

#### Step 1: Install Python
1. Go to: https://www.python.org/downloads/
2. Download Python 3.8 or later
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

#### Step 2: Install Dependencies
Open Command Prompt and run:
```bash
pip install PyQt5 pydantic pyinstaller
```

#### Step 3: Build Executable
```bash
pyinstaller --name=Course_Link_Getter --windowed --onefile --icon=course_link_getter/assets/icon.ico --add-data="course_link_getter/assets;courses_link_getter/assets" --add-data="course_link_getter/core;courses_link_getter/core" --add-data="course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.sip --clean course_link_getter/launch_pyqt5.py
```

## 🔧 Troubleshooting

### "Python was not found"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart Command Prompt after installation

### "'pip' is not recognized"
- Run: `python -m ensurepip --upgrade`
- Or reinstall Python with PATH option

### "Failed to install requirements"
- Check your internet connection
- Try: `pip install --upgrade pip`
- Then try installing requirements again

### "Build failed"
- Make sure all dependencies are installed
- Check the error messages for specific issues
- Try running the build command manually

## 📋 What you'll get

After successful build:
- `Course_Link_Getter.exe` - Single executable file (~40-50MB)
- No installation required - just double-click to run
- All 26 courses included
- Modern UI with search, filter, copy, and export features

## 🎯 System Requirements

- **Windows 10** or later
- **Python 3.8+** (for building)
- **Internet connection** (for downloading dependencies)
- **~100MB free space** (for build process)

## 🚀 Distribution

Once you have the .exe file:
1. **Share** the .exe file with anyone
2. **No installation** required - just double-click
3. **Works offline** - no internet needed
4. **Cross-platform** - works on any Windows 10+ computer

## 📞 Support

If you still have issues:
1. Check the error messages carefully
2. Make sure Python is properly installed
3. Try the manual build steps
4. Visit: https://github.com/HulkBetii/GetLink

---
**Course Link Getter v1.0** - Built with Python and PyQt5
"""
    
    with open("WINDOWS_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    print("✅ Created WINDOWS_INSTRUCTIONS.txt")

def create_complete_package():
    """Create complete package with all options"""
    print("📦 Creating complete Windows package...")
    
    # Create package directory
    package_dir = Path("Course_Link_Getter_Complete_Windows")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy all necessary files
    files_to_copy = [
        "course_link_getter/",
        "build_windows_exe.py",
        "build_windows_exe.bat",
        "requirements.txt",
        "WINDOWS_INSTRUCTIONS.txt"
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, package_dir / item)
                print(f"✅ Copied directory: {item}")
            else:
                shutil.copy2(item, package_dir / item)
                print(f"✅ Copied file: {item}")
    
    # Create improved build script
    build_script = """@echo off
echo 🪟 Course Link Getter - Windows EXE Builder
echo ==========================================
echo.
echo This will create a single .exe file for Windows.
echo.
echo Requirements:
echo - Python 3.8+ installed
echo - Internet connection for pip installs
echo.
echo Checking system requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, restart this script.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo.
    echo Trying to install pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pip
        echo Please install pip manually or reinstall Python
        pause
        exit /b 1
    )
)

echo ✅ pip found
pip --version
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ Requirements installed
echo.

echo Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ❌ Failed to install PyInstaller
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ PyInstaller installed
echo.

echo Building Windows executable...
python build_windows_exe.py
if %errorlevel% neq 0 (
    echo ❌ Build failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📁 Check the 'dist' folder for your .exe file
echo.
echo 🎉 Your Course_Link_Getter.exe is ready!
echo You can now share this .exe file with anyone.
echo.
pause
"""
    
    with open(package_dir / "BUILD_WINDOWS_EXE.bat", "w") as f:
        f.write(build_script)
    
    print("✅ Created BUILD_WINDOWS_EXE.bat")
    
    # Create ZIP package
    import zipfile
    zip_path = "Course_Link_Getter_Complete_Windows.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created complete package: {zip_path}")
    
    # Clean up
    shutil.rmtree(package_dir)
    
    return zip_path

def main():
    """Main function"""
    print("🪟 Course Link Getter Windows Package Creator")
    print("=" * 60)
    
    # Create Windows instructions
    create_windows_instructions()
    
    # Create complete package
    zip_path = create_complete_package()
    
    print(f"\n🎉 Complete Windows package created!")
    print(f"📁 Package: {zip_path}")
    print(f"📊 Size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
    print(f"\n🚀 Features:")
    print(f"✅ Improved error handling")
    print(f"✅ Step-by-step instructions")
    print(f"✅ Automatic dependency checking")
    print(f"✅ Clear error messages")
    print(f"✅ Troubleshooting guide")
    print(f"\n📋 Instructions:")
    print(f"1. Send {zip_path} to Windows user")
    print(f"2. They extract and run BUILD_WINDOWS_EXE.bat")
    print(f"3. Script will guide them through any issues")
    print(f"4. They get Course_Link_Getter.exe")
    
    return True

if __name__ == "__main__":
    main()
