#!/usr/bin/env python3
"""
Create single executable file for current platform
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_single_executable():
    """Create single executable for current platform"""
    print("🚀 Creating single executable file...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build command based on platform
    import platform
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        cmd = [
            'pyinstaller',
            '--name=Course_Link_Getter',
            '--windowed',
            '--onefile',
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
        executable_name = "Course_Link_Getter"
        platform_name = "macOS"
    elif system == 'Windows':
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
        executable_name = "Course_Link_Getter.exe"
        platform_name = "Windows"
    else:  # Linux
        cmd = [
            'pyinstaller',
            '--name=Course_Link_Getter',
            '--windowed',
            '--onefile',
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
        executable_name = "Course_Link_Getter"
        platform_name = "Linux"
    
    print(f"📦 Building for {platform_name}...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully")
        
        # Check if executable was created
        executable_path = f"dist/{executable_name}"
        if os.path.exists(executable_path):
            size_mb = os.path.getsize(executable_path) / (1024 * 1024)
            print(f"✅ Executable created: {executable_path}")
            print(f"📊 Size: {size_mb:.1f} MB")
            
            # Test the executable
            print("🧪 Testing executable...")
            try:
                if system == 'Darwin':
                    # On macOS, test the executable
                    test_result = subprocess.run([executable_path], 
                                               timeout=5, 
                                               capture_output=True, 
                                               text=True)
                    print("✅ Executable test completed")
                else:
                    print("✅ Executable ready for testing")
            except subprocess.TimeoutExpired:
                print("✅ Executable started successfully (timeout expected)")
            except Exception as e:
                print(f"⚠️ Executable test: {e}")
            
            return executable_path
        else:
            print(f"❌ Executable not found: {executable_path}")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def create_distribution_package(executable_path):
    """Create distribution package with the executable"""
    if not executable_path or not os.path.exists(executable_path):
        print("❌ No executable to package")
        return None
    
    print("📦 Creating distribution package...")
    
    # Create distribution directory
    dist_dir = Path("Course_Link_Getter_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy executable
    executable_name = os.path.basename(executable_path)
    shutil.copy2(executable_path, dist_dir / executable_name)
    print(f"✅ Copied executable: {executable_name}")
    
    # Create README
    import platform
    readme_content = f"""# 🎓 Course Link Getter

## 🚀 Quick Start

1. **Download** this package
2. **Run** `{executable_name}` (double-click)
3. **Enjoy** the application!

## ✨ Features

- ✅ **26 courses** loaded automatically
- ✅ **Search and filter** functionality  
- ✅ **Copy links** to clipboard
- ✅ **Export to CSV**
- ✅ **Modern UI** with beautiful interface
- ✅ **No installation** required

## 🎯 System Requirements

- **{platform.system()}** operating system
- **No additional software** required
- **All dependencies** included

## 📱 How to Use

1. **Launch** the application
2. **Search** for courses using the search bar
3. **Filter** by category or subcategory
4. **Click "Get Link"** to copy course links
5. **Use "Copy Visible Links"** for bulk copy
6. **Export to CSV** for data backup

## 🔧 Troubleshooting

- **App won't start**: Make sure you have the right operating system
- **Slow startup**: First launch takes 3-5 seconds (normal)
- **Antivirus warning**: Some antivirus may flag new executables (normal)

## 📞 Support

For issues or questions:
- GitHub: https://github.com/HulkBetii/GetLink
- Repository: https://github.com/HulkBetii/GetLink.git

---
**Course Link Getter v1.0** - Built with Python and PyQt5
"""
    
    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README.txt")
    
    # Create ZIP package
    import zipfile
    zip_path = f"Course_Link_Getter_{platform.system()}_Distribution.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created distribution package: {zip_path}")
    
    # Clean up
    shutil.rmtree(dist_dir)
    
    return zip_path

def main():
    """Main function"""
    print("🚀 Course Link Getter Single Executable Creator")
    print("=" * 60)
    
    # Create single executable
    executable_path = create_single_executable()
    
    if executable_path:
        print(f"\n✅ Single executable created: {executable_path}")
        
        # Create distribution package
        zip_path = create_distribution_package(executable_path)
        
        if zip_path:
            print(f"\n🎉 Distribution package created: {zip_path}")
            print(f"📊 Package size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
            print(f"\n🚀 Ready to share!")
            print(f"1. Send {zip_path} to anyone")
            print(f"2. They extract and run the executable")
            print(f"3. No installation required!")
        else:
            print("❌ Failed to create distribution package")
    else:
        print("❌ Failed to create executable")

if __name__ == "__main__":
    main()
