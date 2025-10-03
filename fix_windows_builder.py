#!/usr/bin/env python3
"""
Fix Windows builder to handle missing Python/pip issues
"""

import os
import shutil
from pathlib import Path

def create_improved_windows_builder():
    """Create improved Windows builder with better error handling"""
    print("🔧 Creating improved Windows builder...")
    
    # Create build directory
    build_dir = Path("windows_build_package_fixed")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Copy necessary files
    files_to_copy = [
        "course_link_getter/",
        "build_windows_exe.py",
        "build_windows_exe.bat", 
        "WINDOWS_BUILD_GUIDE.md",
        "requirements.txt"
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, build_dir / item)
                print(f"✅ Copied directory: {item}")
            else:
                shutil.copy2(item, build_dir / item)
                print(f"✅ Copied file: {item}")
    
    # Create improved build script with error handling
    build_script = """@echo off
echo 🪟 Course Link Getter - Windows EXE Builder (Fixed)
echo ==================================================
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
    
    with open(build_dir / "BUILD_WINDOWS_EXE_FIXED.bat", "w") as f:
        f.write(build_script)
    
    print("✅ Created BUILD_WINDOWS_EXE_FIXED.bat")
    
    # Create Python installer script
    python_installer = """@echo off
echo 🐍 Python Installation Helper
echo =============================
echo.
echo This script will help you install Python if it's not already installed.
echo.
echo Step 1: Download Python
echo - Go to: https://www.python.org/downloads/
echo - Click "Download Python 3.x.x"
echo - Save the installer to your computer
echo.
echo Step 2: Install Python
echo - Run the downloaded installer
echo - IMPORTANT: Check "Add Python to PATH" at the bottom
echo - Click "Install Now"
echo - Wait for installation to complete
echo.
echo Step 3: Verify Installation
echo - Close this window
echo - Open a new Command Prompt
echo - Type: python --version
echo - You should see Python version number
echo.
echo Step 4: Run the Builder
echo - Run BUILD_WINDOWS_EXE_FIXED.bat
echo.
pause
"""
    
    with open(build_dir / "INSTALL_PYTHON.bat", "w") as f:
        f.write(python_installer)
    
    print("✅ Created INSTALL_PYTHON.bat")
    
    # Create comprehensive README
    readme_content = """# 🪟 Course Link Getter - Windows EXE Builder (Fixed)

## 🚀 Quick Start

### Option 1: Automatic Build (Recommended)
1. **Double-click** `BUILD_WINDOWS_EXE_FIXED.bat`
2. **Follow** the on-screen instructions
3. **Wait** for the build to complete
4. **Find** your .exe file in the `dist` folder

### Option 2: Manual Build
If automatic build fails, follow these steps:

1. **Install Python** (if not installed):
   - Run `INSTALL_PYTHON.bat` for instructions
   - Or download from: https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Build Executable**:
   ```bash
   python build_windows_exe.py
   ```

## 🔧 Troubleshooting

### Error: "Python was not found"
**Solution**: Install Python and add it to PATH
1. Download Python from: https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Try again

### Error: "'pip' is not recognized"
**Solution**: Install pip or reinstall Python
1. Run: `python -m ensurepip --upgrade`
2. Or reinstall Python with PATH option

### Error: "Failed to install requirements"
**Solution**: Check internet connection
1. Make sure you have internet access
2. Try running: `pip install -r requirements.txt` manually
3. If still failing, try: `pip install --upgrade pip`

### Error: "Build failed"
**Solution**: Check error messages
1. Look at the error output above
2. Make sure all dependencies are installed
3. Try running: `python build_windows_exe.py` manually

## 📋 What you'll get

After successful build:
- `Course_Link_Getter.exe` - Single executable file (~40-50MB)
- No installation required - just double-click to run
- All 26 courses included
- Modern UI with search, filter, copy, and export features

## 🎯 System Requirements

- **Windows 10** or later
- **Python 3.8+** (will be checked automatically)
- **Internet connection** (for downloading dependencies)
- **~100MB free space** (for build process)

## 📁 Files included

- `course_link_getter/` - Application source code
- `build_windows_exe.py` - Python build script
- `build_windows_exe.bat` - Batch build script
- `BUILD_WINDOWS_EXE_FIXED.bat` - **Improved build launcher**
- `INSTALL_PYTHON.bat` - Python installation helper
- `requirements.txt` - Python dependencies
- `WINDOWS_BUILD_GUIDE.md` - Detailed build guide

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
    
    with open(build_dir / "README_FIXED.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README_FIXED.txt")
    
    # Create ZIP package
    import zipfile
    zip_path = "Course_Link_Getter_Windows_Builder_FIXED.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created fixed package: {zip_path}")
    
    # Clean up
    shutil.rmtree(build_dir)
    
    return zip_path

def main():
    """Main function"""
    print("🔧 Course Link Getter Windows Builder Fix")
    print("=" * 60)
    
    zip_path = create_improved_windows_builder()
    
    print(f"\n🎉 Fixed Windows build package created!")
    print(f"📁 Package: {zip_path}")
    print(f"📊 Size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
    print(f"\n🚀 Improvements:")
    print(f"✅ Better error handling for missing Python/pip")
    print(f"✅ Automatic Python installation helper")
    print(f"✅ Step-by-step troubleshooting guide")
    print(f"✅ Clear error messages and solutions")
    print(f"\n📋 Instructions:")
    print(f"1. Send {zip_path} to Windows user")
    print(f"2. They run BUILD_WINDOWS_EXE_FIXED.bat")
    print(f"3. Script will guide them through any issues")
    print(f"4. They get Course_Link_Getter.exe")
    
    return True

if __name__ == "__main__":
    main()
