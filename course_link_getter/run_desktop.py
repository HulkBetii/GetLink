#!/usr/bin/env python3
"""
Desktop App Launcher - Course Link Getter
Tries PyQt6 first, falls back to PyQt5, then web interface
"""

import sys
import subprocess
from pathlib import Path

def try_pyqt6():
    """Try to run PyQt6 version"""
    try:
        print("🔄 Trying PyQt6 desktop app...")
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        
        app = QApplication(sys.argv)
        app.setApplicationName("Course Link Getter")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CourseLinkGetter")
        
        # Enable high DPI scaling
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Import and create main window
        from ui.main_window import MainWindow
        window = MainWindow()
        window.show()
        
        print("✅ PyQt6 desktop app started successfully!")
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ PyQt6 not available: {e}")
        return False
    except Exception as e:
        print(f"❌ PyQt6 app failed: {e}")
        return False

def try_pyqt5():
    """Try to run PyQt5 version"""
    try:
        print("🔄 Trying PyQt5 desktop app...")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        app = QApplication(sys.argv)
        app.setApplicationName("Course Link Getter")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CourseLinkGetter")
        
        # Enable high DPI scaling
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Import and create main window
        from ui_pyqt5.main_window import MainWindow
        window = MainWindow()
        window.show()
        
        print("✅ PyQt5 desktop app started successfully!")
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ PyQt5 not available: {e}")
        return False
    except Exception as e:
        print(f"❌ PyQt5 app failed: {e}")
        return False

def start_web_app():
    """Start web interface as fallback"""
    print("🌐 Starting web interface...")
    try:
        from web_app import main
        main()
    except Exception as e:
        print(f"❌ Web app failed: {e}")
        print("💡 Try manually: cd course_link_getter && python web_app.py")

def main():
    """Main launcher function"""
    print("🚀 Course Link Getter - Desktop App Launcher")
    print("=" * 50)
    
    # Try PyQt6 first
    if try_pyqt6():
        return
    
    # Try PyQt5 as fallback
    if try_pyqt5():
        return
    
    # Fall back to web interface
    print("⚠️  Desktop apps not available, starting web interface...")
    start_web_app()

if __name__ == "__main__":
    main()
