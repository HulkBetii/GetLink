#!/usr/bin/env python3
"""
Create Windows .exe build instructions and prepare files
"""

import os
import shutil
from pathlib import Path

def create_windows_build_package():
    """Create a package for building Windows .exe"""
    print("🪟 Creating Windows .exe build package...")
    
    # Create build directory
    build_dir = Path("windows_build_package")
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
    
    # Create simple build script
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
pause
echo.
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller
echo.
echo Building Windows executable...
python build_windows_exe.py
echo.
echo ✅ Build completed!
echo 📁 Check the 'dist' folder for your .exe file
echo.
pause
"""
    
    with open(build_dir / "BUILD_WINDOWS_EXE.bat", "w") as f:
        f.write(build_script)
    
    print("✅ Created BUILD_WINDOWS_EXE.bat")
    
    # Create README for Windows users
    readme_content = """# 🪟 Course Link Getter - Windows EXE Builder

## 🚀 Quick Start

1. **Download** this package to your Windows computer
2. **Double-click** `BUILD_WINDOWS_EXE.bat`
3. **Wait** for the build to complete
4. **Find** your .exe file in the `dist` folder

## 📋 What you'll get

- `Course_Link_Getter.exe` - Single executable file (~40-50MB)
- No installation required - just double-click to run
- All 26 courses included
- Modern UI with search, filter, copy, and export features

## 🔧 Manual Build (if needed)

If the automatic build fails, you can build manually:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python build_windows_exe.py
```

## 📁 Files included

- `course_link_getter/` - Application source code
- `build_windows_exe.py` - Python build script
- `build_windows_exe.bat` - Batch build script
- `BUILD_WINDOWS_EXE.bat` - Simple build launcher
- `requirements.txt` - Python dependencies
- `WINDOWS_BUILD_GUIDE.md` - Detailed build guide

## 🎯 Result

After building, you'll have:
- **Single .exe file** - No installation needed
- **Portable** - Runs on any Windows 10+ computer
- **Self-contained** - All dependencies included
- **26 courses** - Full course catalog
- **Modern UI** - Beautiful interface

## 🚀 Distribution

Once you have the .exe file, you can:
1. **Share** the .exe file with anyone
2. **No installation** required - just double-click
3. **Works offline** - no internet needed
4. **Cross-platform** - works on any Windows 10+ computer

---
**Course Link Getter v1.0** - Built with Python and PyQt5
"""
    
    with open(build_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README.txt")
    
    # Create ZIP package
    import zipfile
    zip_path = "Course_Link_Getter_Windows_Builder.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created package: {zip_path}")
    
    # Clean up
    shutil.rmtree(build_dir)
    
    return zip_path

def main():
    """Main function"""
    print("🪟 Course Link Getter Windows EXE Builder Package")
    print("=" * 60)
    
    zip_path = create_windows_build_package()
    
    print(f"\n🎉 Windows build package created successfully!")
    print(f"📁 Package: {zip_path}")
    print(f"📊 Size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
    print(f"\n🚀 Instructions:")
    print(f"1. Send {zip_path} to someone with Windows")
    print(f"2. They extract the ZIP file")
    print(f"3. They run BUILD_WINDOWS_EXE.bat")
    print(f"4. They get Course_Link_Getter.exe (single file)")
    print(f"5. They can share the .exe with anyone!")
    
    return True

if __name__ == "__main__":
    main()
