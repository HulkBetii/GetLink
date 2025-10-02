#!/usr/bin/env python3
"""
Simple PyQt5 Desktop App Launcher
Fixes import issues and launches the desktop app
"""

import sys
from pathlib import Path

# Add the course_link_getter directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def main():
    """Launch PyQt5 desktop app"""
    try:
        print("🚀 Starting Course Link Getter (PyQt5)...")
        
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        app = QApplication(sys.argv)
        app.setApplicationName("Course Link Getter")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CourseLinkGetter")
        
        # Enable high DPI scaling
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Initialize translations
        from core.translations import init_translations
        init_translations(app)
        
        # Import and create main window
        from ui_pyqt5.main_window import MainWindow
        window = MainWindow()
        window.show()
        
        print("✅ Desktop app started successfully!")
        print("🎓 Course Link Getter is now running...")
        
        # Start event loop
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ PyQt5 not available: {e}")
        print("💡 Install PyQt5: pip install PyQt5")
        return False
    except Exception as e:
        print(f"❌ Desktop app failed: {e}")
        print("💡 Try the web interface: python web_app.py")
        return False

if __name__ == "__main__":
    main()
