from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView,
    QPushButton, QLabel, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal
from PyQt6.QtGui import QAction
from typing import List, Optional
from ...core.models import Course


class CourseTableModel(QAbstractTableModel):
    """Table model for displaying courses."""
    
    def __init__(self, courses: List[Course] = None):
        super().__init__()
        self.courses = courses or []
        self.headers = [
            "Title", "Category", "Subcategory", "Provider", "Tags", "Actions"
        ]
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.courses)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.headers)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        course = self.courses[index.row()]
        col = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:  # Title
                return course.title
            elif col == 1:  # Category
                return course.category
            elif col == 2:  # Subcategory
                return course.subcategory
            elif col == 3:  # Provider
                return course.provider
            elif col == 4:  # Tags
                return ", ".join(course.tags) if course.tags else "N/A"
            elif col == 5:  # Actions
                return "Get Link"
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None
    
    def set_courses(self, courses: List[Course]):
        """Update the courses data."""
        self.beginResetModel()
        self.courses = courses
        self.endResetModel()
    
    def get_course(self, row: int) -> Optional[Course]:
        """Get course at specific row."""
        if 0 <= row < len(self.courses):
            return self.courses[row]
        return None


class ResultsView(QWidget):
    """View for displaying course search results."""
    
    # Signals
    course_link_requested = pyqtSignal(Course)
    course_open_requested = pyqtSignal(Course)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Results header
        header_layout = QHBoxLayout()
        self.results_label = QLabel("Results: 0 courses")
        header_layout.addWidget(self.results_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Table view
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        
        # Set up the model
        self.model = CourseTableModel()
        self.table_view.setModel(self.model)
        
        # Configure columns
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Subcategory
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Provider
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Tags
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Actions
        
        # Connect double-click to get link
        self.table_view.doubleClicked.connect(self._on_double_clicked)
        
        layout.addWidget(self.table_view)
    
    def set_courses(self, courses: List[Course]):
        """Set the courses to display."""
        self.model.set_courses(courses)
        self.results_label.setText(f"Results: {len(courses)} courses")
    
    def _on_double_clicked(self, index: QModelIndex):
        """Handle double-click on table row."""
        course = self.model.get_course(index.row())
        if course:
            self.course_link_requested.emit(course)
    
    def get_selected_courses(self) -> List[Course]:
        """Get currently selected courses."""
        selected_courses = []
        selection = self.table_view.selectionModel()
        if selection:
            for index in selection.selectedRows():
                course = self.model.get_course(index.row())
                if course:
                    selected_courses.append(course)
        return selected_courses
    
    def get_all_visible_courses(self) -> List[Course]:
        """Get all currently visible courses."""
        return self.model.courses.copy()
