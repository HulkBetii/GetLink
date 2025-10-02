from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QMessageBox, QFileDialog, QApplication,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableView,
    QAbstractItemView, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence
from typing import List
import sys
import subprocess
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from .widgets.results_view import CourseTableModel
from core.store import CatalogStore
from core.models import Course
from core.settings import SettingsManager


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.store = CatalogStore()
        self.settings_manager = SettingsManager()
        self.current_courses: List[Course] = []
        
        # Load data first before setting up UI
        self._load_initial_data()
        self._setup_ui()
        self._connect_signals()
    
    def _apply_theme(self):
        """Apply modern white theme to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
                color: #333333;
            }
            
            QWidget {
                background-color: #ffffff;
                color: #333333;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 13px;
            }
            
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #0056CC;
            }
            
            QPushButton:pressed {
                background-color: #004499;
            }
            
            QPushButton:disabled {
                background-color: #E5E5E7;
                color: #8E8E93;
            }
            
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 6px 12px;
                min-height: 20px;
            }
            
            QComboBox:hover {
                border-color: #007AFF;
            }
            
            QComboBox:focus {
                border-color: #007AFF;
                outline: none;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 20px;
            }
            
            QLineEdit:hover {
                border-color: #007AFF;
            }
            
            QLineEdit:focus {
                border-color: #007AFF;
                outline: none;
            }
            
            QTableView {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                gridline-color: #E5E5E7;
                selection-background-color: #E3F2FD;
                alternate-background-color: #F8F9FA;
            }
            
            QTableView::item {
                padding: 8px;
                border: none;
            }
            
            QTableView::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QHeaderView::section {
                background-color: #F8F9FA;
                color: #333333;
                border: none;
                border-bottom: 1px solid #D1D1D6;
                border-right: 1px solid #E5E5E7;
                padding: 8px;
                font-weight: 600;
            }
            
            QGroupBox {
                font-weight: 600;
                color: #333333;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #ffffff;
            }
            
            QLabel {
                color: #333333;
            }
            
            QStatusBar {
                background-color: #F8F9FA;
                border-top: 1px solid #D1D1D6;
                color: #666666;
            }
            
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #D1D1D6;
                color: #333333;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
            }
            
            QMenuBar::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QMenu {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                color: #333333;
            }
            
            QMenu::item {
                padding: 8px 16px;
            }
            
            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
    
    def _setup_ui(self):
        """Setup the main user interface."""
        self.setWindowTitle("Course Link Getter")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply modern theme
        self._apply_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header section
        self._create_header(main_layout)
        
        # Filter and action panel (horizontal)
        self._create_filter_panel(main_layout)
        
        # Results section
        self._create_results_section(main_layout)
        
        # Menu bar
        self._create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _create_header(self, parent_layout):
        """Create the header section with title and icon."""
        header_widget = QWidget()
        header_widget.setFixedHeight(120)
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: white;
            }
        """)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(8)
        
        # Title with icon
        title_layout = QHBoxLayout()
        
        # Icon (using a simple label with emoji for now)
        icon_label = QLabel("🎓")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: white;
            }
        """)
        title_layout.addWidget(icon_label)
        
        # Title text
        title_label = QLabel("Course Link Getter")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                margin-left: 10px;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        
        # Subtitle
        subtitle_label = QLabel("Browse and access course links through hierarchical categories")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #BDC3C7;
                margin-left: 42px;
            }
        """)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget)
    
    def _create_filter_panel(self, parent_layout):
        """Create the horizontal filter and action panel."""
        filter_widget = QWidget()
        filter_widget.setFixedHeight(80)
        filter_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-bottom: 1px solid #E5E5E5;
            }
        """)
        
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(20, 15, 20, 15)
        filter_layout.setSpacing(15)
        
        # Search section
        search_label = QLabel("Search:")
        search_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.setFixedWidth(200)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007AFF;
                outline: none;
            }
        """)
        filter_layout.addWidget(self.search_input)
        
        # Category section
        category_label = QLabel("Category:")
        category_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        filter_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setFixedWidth(150)
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #007AFF;
            }
        """)
        filter_layout.addWidget(self.category_combo)
        
        # Subcategory section
        subcategory_label = QLabel("Subcategory:")
        subcategory_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        filter_layout.addWidget(subcategory_label)
        
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.setFixedWidth(150)
        self.subcategory_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #007AFF;
            }
        """)
        filter_layout.addWidget(self.subcategory_combo)
        
        # Add spacer
        filter_layout.addStretch()
        
        # Action buttons
        self.show_all_btn = QPushButton("Show All")
        self.show_all_btn.setFixedSize(100, 35)
        self.show_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        filter_layout.addWidget(self.show_all_btn)
        
        self.copy_links_btn = QPushButton("Copy All Links")
        self.copy_links_btn.setFixedSize(120, 35)
        self.copy_links_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        filter_layout.addWidget(self.copy_links_btn)
        
        self.export_csv_btn = QPushButton("Export CSV")
        self.export_csv_btn.setFixedSize(100, 35)
        self.export_csv_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        filter_layout.addWidget(self.export_csv_btn)
        
        parent_layout.addWidget(filter_widget)
    
    def _create_results_section(self, parent_layout):
        """Create the results section with table."""
        results_widget = QWidget()
        results_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(10)
        
        # Results header
        results_header = QHBoxLayout()
        
        self.results_count_label = QLabel("Loaded 0 courses")
        self.results_count_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #333333;
            }
        """)
        results_header.addWidget(self.results_count_label)
        results_header.addStretch()
        
        results_layout.addLayout(results_header)
        
        # Table view
        self.table_view = QTableView()
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: white;
                border: 1px solid #E5E5E5;
                border-radius: 8px;
                gridline-color: #F0F0F0;
                selection-background-color: #E3F2FD;
                alternate-background-color: #FAFAFA;
            }
            QTableView::item {
                padding: 12px 8px;
                border: none;
                font-size: 13px;
            }
            QTableView::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QTableView::item:hover {
                background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-right: 1px solid #34495E;
                padding: 12px 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QHeaderView::section:hover {
                background-color: #34495E;
            }
        """)
        
        # Set up the model
        self.model = CourseTableModel()
        self.table_view.setModel(self.model)
        
        # Configure columns
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Subcategory
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Provider
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Tags
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Action
        
        # Enable sorting and selection
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        results_layout.addWidget(self.table_view)
        parent_layout.addWidget(results_widget)
    
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
        # Search input
        self.search_input.textChanged.connect(self._on_search_changed)
        
        # Category and subcategory dropdowns
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        self.subcategory_combo.currentTextChanged.connect(self._on_subcategory_changed)
        
        # Action buttons
        self.show_all_btn.clicked.connect(self._show_all_courses)
        self.export_csv_btn.clicked.connect(self._export_to_csv)
        self.copy_links_btn.clicked.connect(self._copy_all_links)
        
        # Table view signals
        self.table_view.clicked.connect(self._on_table_clicked)
        
        # Load initial data into the UI
        self._load_categories()
        self._on_filters_changed()
    
    def _load_categories(self):
        """Load categories into the dropdown."""
        categories = self.store.list_categories()
        
        # Clear and populate category combo
        self.category_combo.clear()
        self.category_combo.addItem("All Categories")
        
        for category in categories:
            self.category_combo.addItem(category.name)
        
        # Clear subcategory combo initially
        self.subcategory_combo.clear()
        self.subcategory_combo.addItem("All Subcategories")
        self.subcategory_combo.setEnabled(False)
    
    def _on_search_changed(self, text):
        """Handle search text change."""
        self._on_filters_changed()
    
    def _on_category_changed(self, category_name):
        """Handle category selection change."""
        if category_name == "All Categories":
            self.subcategory_combo.clear()
            self.subcategory_combo.addItem("All Subcategories")
            self.subcategory_combo.setEnabled(False)
        else:
            # Find the selected category and populate subcategories
            categories = self.store.list_categories()
            for category in categories:
                if category.name == category_name:
                    self.subcategory_combo.clear()
                    self.subcategory_combo.addItem("All Subcategories")
                    for subcategory in category.subcategories:
                        self.subcategory_combo.addItem(subcategory)
                    self.subcategory_combo.setEnabled(True)
                    break
        
        self._on_filters_changed()
    
    def _on_subcategory_changed(self, subcategory_name):
        """Handle subcategory selection change."""
        self._on_filters_changed()
    
    def _on_table_clicked(self, index):
        """Handle table cell click."""
        if index.column() == 5:  # Action column
            course = self.model.get_course(index.row())
            if course:
                self._copy_course_link(course)
    
    def _load_initial_data(self):
        """Load initial data and populate the interface."""
        # Load JSON data - use correct path (go up one level from ui_pyqt5)
        json_path = Path(__file__).parent.parent / "assets" / "catalog.sample.json"
        if not self.store.load_from_json(str(json_path)):
            print(f"Warning: Failed to load catalog from {json_path}")
            return False
        
        print(f"✅ Loaded {len(self.store.list_all())} courses from catalog")
        return True
    
    def _on_filters_changed(self):
        """Handle any filter change - get filtered courses and update results."""
        # Get current filter values
        search_text = self.search_input.text().strip()
        category = self.category_combo.currentText()
        subcategory = self.subcategory_combo.currentText()
        
        # Apply filters
        courses = self.store.filter(
            category=category if category != "All Categories" else None,
            subcategory=subcategory if subcategory != "All Subcategories" else None,
            text=search_text if search_text else None
        )
        
        self.current_courses = courses
        self.model.set_courses(courses)
        
        # Update results count
        self.results_count_label.setText(f"Loaded {len(courses)} courses")
        
        # Update button states
        self.export_csv_btn.setEnabled(len(courses) > 0)
        self.copy_links_btn.setEnabled(len(courses) > 0)
        
        # Update status with filtered/total information
        total_courses = len(self.store.list_all())
        if len(courses) == total_courses:
            self.statusBar().showMessage(f"{total_courses} total courses")
        else:
            self.statusBar().showMessage(f"{len(courses)} results (filtered from {total_courses} total)")
    
    def _show_all_courses(self):
        """Show all courses without filters."""
        # Clear all filters
        self.search_input.clear()
        self.category_combo.setCurrentText("All Categories")
        self.subcategory_combo.setCurrentText("All Subcategories")
        self.subcategory_combo.setEnabled(False)
        self._on_filters_changed()
    
    def _copy_course_link(self, course: Course):
        """Copy a single course link to clipboard."""
        if self._copy_to_clipboard(course.link):
            self.statusBar().showMessage(f"Copied link for: {course.title}")
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
        else:
            self._show_error("Failed to copy links to clipboard")
    
    def _open_selected_courses(self):
        """Open selected courses in browser with confirmation."""
        # Get selected rows from table view
        selected_indexes = self.table_view.selectionModel().selectedRows()
        selected_courses = []
        
        for index in selected_indexes:
            course = self.model.get_course(index.row())
            if course:
                selected_courses.append(course)
        
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
