#!/usr/bin/env python3
"""
Rebuild package with data verification
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
    files_to_clean = ['*.spec', '*.dmg']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
    
    # Remove old DMG
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

def build_package():
    """Build the package with PyInstaller"""
    print("📦 Building package with PyInstaller...")
    
    cmd = [
        'pyinstaller',
        '--name=Course Link Getter',
        '--windowed',
        '--onedir',
        '--icon=course_link_getter/assets/icon.icns',
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

def create_dmg():
    """Create DMG installer"""
    print("📦 Creating DMG installer...")
    
    if not os.path.exists('dist/Course Link Getter.app'):
        print("❌ App bundle not found")
        return False
    
    cmd = [
        'hdiutil', 'create',
        '-volname', 'Course Link Getter',
        '-srcfolder', 'dist/Course Link Getter.app',
        '-ov', '-format', 'UDZO',
        'Course_Link_Getter_macOS.dmg'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ DMG created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG creation failed: {e}")
        return False

def verify_package():
    """Verify the created package"""
    print("🔍 Verifying package...")
    
    # Check DMG exists
    if not os.path.exists('Course_Link_Getter_macOS.dmg'):
        print("❌ DMG file not found")
        return False
    
    print("✅ DMG file created")
    
    # Mount and check contents
    try:
        result = subprocess.run(['hdiutil', 'attach', 'Course_Link_Getter_macOS.dmg'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to mount DMG: {result.stderr}")
            return False
        
        # Find mounted volume
        volume_path = None
        for line in result.stdout.split('\n'):
            if 'Course Link Getter' in line and '/Volumes/' in line:
                parts = line.split()
                for part in parts:
                    if '/Volumes/' in part:
                        volume_path = part
                        break
                break
        
        if not volume_path:
            print("❌ Could not find mounted volume")
            return False
        
        # Check app bundle
        app_path = f"{volume_path}/Course Link Getter.app"
        if not os.path.exists(app_path):
            print(f"❌ App bundle not found: {app_path}")
            return False
        
        # Check catalog file
        catalog_path = f"{app_path}/Contents/Resources/courses_link_getter/assets/catalog.sample.json"
        if not os.path.exists(catalog_path):
            print(f"❌ Catalog file not found: {catalog_path}")
            return False
        
        print("✅ Package verification passed")
        return True
        
    except Exception as e:
        print(f"❌ Package verification failed: {e}")
        return False

def main():
    """Main rebuild function"""
    print("🔄 Course Link Getter Package Rebuild")
    print("=" * 50)
    
    # Clean previous builds
    clean_build()
    print()
    
    # Verify data files
    if not verify_data():
        print("❌ Data verification failed")
        return False
    print()
    
    # Build package
    if not build_package():
        print("❌ Package build failed")
        return False
    print()
    
    # Create DMG
    if not create_dmg():
        print("❌ DMG creation failed")
        return False
    print()
    
    # Verify package
    if not verify_package():
        print("❌ Package verification failed")
        return False
    print()
    
    print("🎉 Package rebuild completed successfully!")
    print("📁 DMG file: Course_Link_Getter_macOS.dmg")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
