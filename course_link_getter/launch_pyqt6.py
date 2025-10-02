#!/usr/bin/env python3
"""
Simple PyQt6 Desktop App Launcher
Attempts to launch PyQt6 version with better error handling
"""

import sys
from pathlib import Path

# Add the course_link_getter directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def main():
    """Launch PyQt6 desktop app"""
    try:
        print("🚀 Starting Course Link Getter (PyQt6)...")
        
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
        
        print("✅ Desktop app started successfully!")
        print("🎓 Course Link Getter is now running...")
        
        # Start event loop
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ PyQt6 not available: {e}")
        print("💡 Install PyQt6: pip install PyQt6")
        return False
    except Exception as e:
        print(f"❌ Desktop app failed: {e}")
        print("💡 Try PyQt5 version: python launch_pyqt5.py")
        print("💡 Or try web interface: python web_app.py")
        return False

if __name__ == "__main__":
    main()
