#!/bin/bash

# Build script for macOS
echo "🍎 Building Course Link Getter for macOS..."

# Clean previous builds
rm -rf dist/
rm -rf build/
rm -rf *.spec

# Create macOS app bundle
pyinstaller \
    --name="Course Link Getter" \
    --windowed \
    --onedir \
    --icon=course_link_getter/assets/icon.icns \
    --add-data="course_link_getter/assets:courses_link_getter/assets" \
    --add-data="course_link_getter/core:courses_link_getter/core" \
    --add-data="course_link_getter/ui_pyqt5:courses_link_getter/ui_pyqt5" \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=PyQt5.sip \
    --clean \
    course_link_getter/launch_pyqt5.py

# Create DMG if successful
if [ -d "dist/Course Link Getter.app" ]; then
    echo "✅ macOS app created successfully!"
    echo "📁 App location: dist/Course Link Getter.app"
    
    # Create DMG
    echo "📦 Creating DMG installer..."
    hdiutil create -volname "Course Link Getter" -srcfolder "dist/Course Link Getter.app" -ov -format UDZO "Course_Link_Getter_macOS.dmg"
    echo "✅ DMG created: Course_Link_Getter_macOS.dmg"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 macOS build completed!"
