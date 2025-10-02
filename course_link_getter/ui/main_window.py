from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QKeySequence
from typing import List
import sys
import subprocess
import csv
from datetime import datetime

from .widgets import FiltersPanel, ResultsView, Toolbar
from ..core import CatalogStore, Course


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.store = CatalogStore()
        self.current_courses: List[Course] = []
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()
    
    def _setup_ui(self):
        """Setup the main user interface."""
        self.setWindowTitle("Course Link Getter")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Toolbar
        self.toolbar = Toolbar()
        main_layout.addWidget(self.toolbar)
        
        # Splitter for filters and results
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Filters panel (left)
        self.filters_panel = FiltersPanel()
        self.filters_panel.setMaximumWidth(300)
        self.filters_panel.setMinimumWidth(250)
        splitter.addWidget(self.filters_panel)
        
        # Results view (right)
        self.results_view = ResultsView()
        splitter.addWidget(self.results_view)
        
        # Set splitter proportions (30% filters, 70% results)
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # Menu bar
        self._create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Export action
        export_action = QAction("&Export to CSV...", self)
        export_action.setShortcut(QKeySequence.StandardKey.Save)
        export_action.triggered.connect(self._export_to_csv)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _connect_signals(self):
        """Connect all signals and slots."""
        # Filters panel signals
        self.filters_panel.category_changed.connect(self._on_category_changed)
        self.filters_panel.subcategory_changed.connect(self._on_subcategory_changed)
        self.filters_panel.search_changed.connect(self._on_search_changed)
        self.filters_panel.show_all_clicked.connect(self._show_all_courses)
        
        # Results view signals
        self.results_view.course_link_requested.connect(self._copy_course_link)
        
        # Toolbar signals
        self.toolbar.show_all_clicked.connect(self._show_all_courses)
        self.toolbar.export_csv_clicked.connect(self._export_to_csv)
        self.toolbar.copy_links_clicked.connect(self._copy_all_links)
    
    def _load_initial_data(self):
        """Load initial data and populate the interface."""
        # Load JSON data
        json_path = "assets/catalog.sample.json"
        if not self.store.load_from_json(json_path):
            QMessageBox.warning(self, "Warning", f"Failed to load catalog from {json_path}")
            return
        
        # Load categories
        categories = self.store.list_categories()
        self.filters_panel.set_categories(categories)
        
        # Load all courses initially
        self._show_all_courses()
    
    def _on_category_changed(self, category_name: str):
        """Handle category selection change."""
        self._apply_filters()
    
    def _on_subcategory_changed(self, subcategory_name: str):
        """Handle subcategory selection change."""
        self._apply_filters()
    
    def _on_search_changed(self, search_text: str):
        """Handle search text change."""
        self._apply_filters()
    
    def _apply_filters(self):
        """Apply current filters and update results."""
        filters = self.filters_panel.get_current_filters()
        
        # Use the new filter method
        courses = self.store.filter(
            category=filters['category'],
            subcategory=filters['subcategory'],
            text=filters['search'] if filters['search'] else None
        )
        
        self.current_courses = courses
        self.results_view.set_courses(courses)
        
        # Update toolbar state
        self.toolbar.set_export_enabled(len(courses) > 0)
        self.toolbar.set_copy_links_enabled(len(courses) > 0)
        
        # Update status
        self.statusBar().showMessage(f"Showing {len(courses)} courses")
    
    def _show_all_courses(self):
        """Show all courses without filters."""
        self.filters_panel.clear_filters()
        self._apply_filters()
    
    def _copy_course_link(self, course: Course):
        """Copy a single course link to clipboard."""
        if self._copy_to_clipboard(course.link):
            self.statusBar().showMessage(f"Copied link for: {course.title}")
            self.toolbar.set_status(f"Copied: {course.title}")
        else:
            self._show_error("Failed to copy link to clipboard")
    
    def _copy_all_links(self):
        """Copy all visible course links to clipboard."""
        if not self.current_courses:
            self._show_error("No courses to copy")
            return
        
        links = [course.link for course in self.current_courses]
        links_text = "\n".join(links)
        
        if self._copy_to_clipboard(links_text):
            self.statusBar().showMessage(f"Copied {len(links)} links to clipboard")
            self.toolbar.set_status(f"Copied {len(links)} links")
        else:
            self._show_error("Failed to copy links to clipboard")
    
    def _copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["pbcopy"], input=text, text=True, check=True)
            elif sys.platform == "win32":  # Windows
                subprocess.run(["clip"], input=text, text=True, check=True)
            else:  # Linux
                subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _export_to_csv(self):
        """Export current courses to CSV file."""
        if not self.current_courses:
            self._show_error("No courses to export")
            return
        
        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Courses to CSV", 
            f"courses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'title', 'category', 'subcategory', 'provider', 'link', 'tags'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in self.current_courses:
                    writer.writerow({
                        'id': course.id,
                        'title': course.title,
                        'category': course.category,
                        'subcategory': course.subcategory,
                        'provider': course.provider,
                        'link': course.link,
                        'tags': ', '.join(course.tags) if course.tags else ''
                    })
            
            self.statusBar().showMessage(f"Exported {len(self.current_courses)} courses to {file_path}")
            self.toolbar.set_status(f"Exported to {file_path}")
            
        except Exception as e:
            self._show_error(f"Failed to export CSV: {str(e)}")
    
    def _show_error(self, message: str):
        """Show an error message."""
        QMessageBox.critical(self, "Error", message)
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Course Link Getter",
            "Course Link Getter v1.0\n\n"
            "A desktop application for browsing and accessing course links "
            "through hierarchical category navigation with clipboard integration "
            "and export capabilities.\n\n"
            "Built with Python and PyQt6."
        )
