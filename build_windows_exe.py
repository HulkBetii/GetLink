#!/usr/bin/env python3
"""
Build Windows executable as single .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    dirs_to_clean = ['dist', 'build', '__pycache__']
    files_to_clean = ['*.spec', '*.exe', '*.zip']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
    
    # Remove old files
    for file in files_to_clean:
        if '*' in file:
            import glob
            for f in glob.glob(file):
                os.remove(f)
                print(f"  Removed {f}")

def verify_data():
    """Verify that all required data files exist"""
    print("🔍 Verifying data files...")
    
    required_files = [
        "course_link_getter/assets/catalog.sample.json",
        "course_link_getter/core/models.py",
        "course_link_getter/core/store.py",
        "course_link_getter/ui_pyqt5/main_window.py",
        "course_link_getter/launch_pyqt5.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    # Check catalog content
    catalog_path = "course_link_getter/assets/catalog.sample.json"
    with open(catalog_path, 'r') as f:
        content = f.read()
        if '"courses"' in content and len(content) > 1000:
            print(f"✅ Catalog contains data ({len(content)} characters)")
            return True
        else:
            print(f"❌ Catalog appears empty or corrupted")
            return False

def build_single_exe():
    """Build single .exe file with PyInstaller"""
    print("📦 Building single .exe file with PyInstaller...")
    
    # Use correct syntax for current platform
    import platform
    if platform.system() == 'Windows':
        # Windows syntax
        cmd = [
            'pyinstaller',
            '--name=Course_Link_Getter',
            '--windowed',
            '--onefile',
            '--icon=course_link_getter/assets/icon.ico',
            '--add-data=course_link_getter/assets;courses_link_getter/assets',
            '--add-data=course_link_getter/core;courses_link_getter/core',
            '--add-data=course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5',
            '--hidden-import=PyQt5.QtCore',
            '--hidden-import=PyQt5.QtGui',
            '--hidden-import=PyQt5.QtWidgets',
            '--hidden-import=PyQt5.sip',
            '--clean',
            'course_link_getter/launch_pyqt5.py'
        ]
    else:
        # macOS/Linux syntax
        cmd = [
            'pyinstaller',
            '--name=Course_Link_Getter',
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
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyInstaller build completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer():
    """Create installer package"""
    print("📦 Creating installer package...")
    
    exe_path = "dist/Course_Link_Getter.exe"
    if not os.path.exists(exe_path):
        print("❌ Executable not found")
        return False
    
    print(f"✅ Executable created: {exe_path}")
    
    # Get file size
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📊 File size: {size_mb:.1f} MB")
    
    # Create a simple installer script
    installer_script = """@echo off
echo Course Link Getter - Windows Installer
echo =====================================
echo.
echo This will install Course Link Getter to your system.
echo.
pause
echo.
echo Installing...
copy "Course_Link_Getter.exe" "%USERPROFILE%\\Desktop\\Course_Link_Getter.exe"
echo.
echo ✅ Installation completed!
echo 📁 Course Link Getter.exe has been copied to your Desktop
echo.
echo You can now run the application from your Desktop.
echo.
pause
"""
    
    with open("install.bat", "w") as f:
        f.write(installer_script)
    
    print("✅ Installer script created: install.bat")
    
    # Create ZIP with installer
    import zipfile
    with zipfile.ZipFile("Course_Link_Getter_Windows_Installer.zip", "w") as zipf:
        zipf.write(exe_path, "Course_Link_Getter.exe")
        zipf.write("install.bat", "install.bat")
        zipf.write("README_Windows.txt", "README.txt")
    
    print("✅ Installer package created: Course_Link_Getter_Windows_Installer.zip")
    return True

def create_readme():
    """Create README for Windows users"""
    readme_content = """# Course Link Getter - Windows

## Quick Installation

1. **Download**: `Course_Link_Getter_Windows_Installer.zip`
2. **Extract**: Unzip the file to any folder
3. **Install**: Double-click `install.bat` to install
4. **Run**: Find `Course_Link_Getter.exe` on your Desktop

## Manual Installation

1. **Download**: `Course_Link_Getter.exe`
2. **Copy**: Move the file to any folder you want
3. **Run**: Double-click `Course_Link_Getter.exe`

## Features

- ✅ 26 courses loaded automatically
- ✅ Search and filter functionality
- ✅ Copy links to clipboard
- ✅ Export to CSV
- ✅ Modern UI with dark theme

## System Requirements

- Windows 10 or later
- No additional software required (all dependencies included)

## Troubleshooting

- **Antivirus warning**: Some antivirus may flag new executables - this is normal
- **Missing DLL**: If you get DLL errors, install Visual C++ Redistributable
- **App won't start**: Make sure you have Windows 10 or later

## Support

For issues or questions, visit: https://github.com/HulkBetii/GetLink

---
Course Link Getter v1.0 - Built with Python and PyQt5
"""
    
    with open("README_Windows.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Windows README created")

def main():
    """Main build function"""
    print("🪟 Course Link Getter Windows EXE Builder")
    print("=" * 50)
    
    # Clean previous builds
    clean_build()
    print()
    
    # Verify data files
    if not verify_data():
        print("❌ Data verification failed")
        return False
    print()
    
    # Build single executable
    if not build_single_exe():
        print("❌ EXE build failed")
        return False
    print()
    
    # Create README
    create_readme()
    print()
    
    # Create installer package
    if not create_installer():
        print("❌ Installer creation failed")
        return False
    print()
    
    print("🎉 Windows EXE build completed successfully!")
    print("📁 Files created:")
    print("  - dist/Course_Link_Getter.exe (single executable)")
    print("  - Course_Link_Getter_Windows_Installer.zip (installer package)")
    print("  - install.bat (installer script)")
    print("  - README_Windows.txt (user guide)")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
