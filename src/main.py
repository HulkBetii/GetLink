#!/usr/bin/env python3
"""
Course Link Getter - Main Application Entry Point

A desktop application for browsing and accessing course links through 
hierarchical category navigation with clipboard integration and export capabilities.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Course Link Getter")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CourseLinkGetter")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
