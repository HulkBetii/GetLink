from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QMessageBox, QFileDialog, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence
from typing import List
import sys
import subprocess
import csv
from datetime import datetime

from .widgets import FiltersPanel, ResultsView, Toolbar
from ..core import CatalogStore, Course
from ..core.settings import SettingsManager


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.store = CatalogStore()
        self.settings_manager = SettingsManager()
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
        splitter = QSplitter(Qt.Horizontal)
        
        # Filters panel (left)
        self.filters_panel = FiltersPanel(self.store, self.settings_manager)
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
        export_action.setShortcut(QKeySequence.Save)
        export_action.triggered.connect(self._export_to_csv)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
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
        self.filters_panel.filters_changed.connect(self._on_filters_changed)
        
        # Results view signals
        self.results_view.course_link_requested.connect(self._copy_course_link)
        
        # Toolbar signals
        self.toolbar.show_all_clicked.connect(self._show_all_courses)
        self.toolbar.export_csv_clicked.connect(self._export_to_csv)
        self.toolbar.copy_links_clicked.connect(self._copy_all_links)
        self.toolbar.open_selected_clicked.connect(self._open_selected_courses)
    
    def _load_initial_data(self):
        """Load initial data and populate the interface."""
        # Load JSON data
        json_path = "assets/catalog.sample.json"
        if not self.store.load_from_json(json_path):
            QMessageBox.warning(self, "Warning", f"Failed to load catalog from {json_path}")
            return
        
        # Load all courses initially
        self._on_filters_changed()
    
    def _on_filters_changed(self):
        """Handle any filter change - get filtered courses and update results."""
        courses = self.filters_panel.get_filtered_courses()
        
        self.current_courses = courses
        self.results_view.set_courses(courses)
        
        # Update toolbar state
        self.toolbar.set_export_enabled(len(courses) > 0)
        self.toolbar.set_copy_links_enabled(len(courses) > 0)
        # Open selected is enabled when there are courses (selection will be checked in the method)
        self.toolbar.set_open_selected_enabled(len(courses) > 0)
        
        # Update status with filtered/total information
        total_courses = len(self.store.list_all())
        if len(courses) == total_courses:
            self.statusBar().showMessage(f"{total_courses} total courses")
        else:
            self.statusBar().showMessage(f"{len(courses)} results (filtered from {total_courses} total)")
    
    def _show_all_courses(self):
        """Show all courses without filters."""
        self.filters_panel._clear_filters()
    
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
    
    def _open_selected_courses(self):
        """Open selected courses in browser with confirmation."""
        selected_courses = self.results_view.get_selected_courses()
        
        if not selected_courses:
            QMessageBox.information(self, "No Selection", "Please select one or more courses to open.")
            return
        
        # Ask for confirmation if more than 5 courses
        if len(selected_courses) > 5:
            reply = QMessageBox.question(
                self, 
                "Confirm Opening Multiple Links",
                f"You are about to open {len(selected_courses)} links in your browser.\n\nThis may open many browser tabs. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # Open each course link
        opened_count = 0
        failed_count = 0
        
        for course in selected_courses:
            try:
                import webbrowser
                webbrowser.open(course.link)
                opened_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to open {course.title}: {e}")
        
        # Show result message
        if failed_count == 0:
            QMessageBox.information(self, "Links Opened", f"Successfully opened {opened_count} links in your browser.")
        else:
            QMessageBox.warning(self, "Partial Success", f"Opened {opened_count} links, failed to open {failed_count} links.")
        
        self.statusBar().showMessage(f"Opened {opened_count} links in browser")
    
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
                # Export only the specified columns: title, category, subcategory, provider, link
                fieldnames = ['title', 'category', 'subcategory', 'provider', 'link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in self.current_courses:
                    writer.writerow({
                        'title': course.title,
                        'category': course.category,
                        'subcategory': course.subcategory,
                        'provider': course.provider,
                        'link': course.link
                    })
            
            QMessageBox.information(self, "Export Complete", f"Exported {len(self.current_courses)} courses to {file_path}")
            self.statusBar().showMessage(f"Exported {len(self.current_courses)} courses to CSV")
            
        except PermissionError:
            QMessageBox.critical(self, "Export Error", "Permission denied. Please choose a different location or close the file if it's open.")
        except OSError as e:
            QMessageBox.critical(self, "Export Error", f"File system error: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {str(e)}")
    
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
            "Built with Python and PyQt5."
        )
