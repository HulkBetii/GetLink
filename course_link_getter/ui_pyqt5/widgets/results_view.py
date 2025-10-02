from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView,
    QPushButton, QLabel, QAbstractItemView, QMessageBox, QMenu,
    QToolTip, QApplication, QStyledItemDelegate, QStyleOptionButton, QStyle
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal, QTimer, QRect, QSize
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence, QPainter, QFontMetrics, QColor, QPen
from typing import List, Optional
import webbrowser
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.models import Course
from core.translations import tr


class ButtonDelegate(QStyledItemDelegate):
    """Custom delegate to render buttons in table cells."""
    
    button_clicked = pyqtSignal(int)  # Emits row index when button is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Make the CTA obvious: add an icon and keep text translatable
        self.button_text = f"🔗  {tr('get_link')}"
        # Colors for normal / hover / pressed states
        self.color_normal = QColor("#007AFF")
        self.color_hover = QColor("#0056CC")
        self.color_pressed = QColor("#004499")
    
    def paint(self, painter, option, index):
        """Paint a prominent CTA button in the cell."""
        if index.column() == 3:  # Actions column
            rect = option.rect.adjusted(4, 4, -4, -4)
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)

            # Determine background color based on state
            bg = self.color_normal
            if option.state & QStyle.State_Sunken:
                bg = self.color_pressed
            elif option.state & QStyle.State_MouseOver:
                bg = self.color_hover

            # Draw rounded rectangle background
            painter.setPen(Qt.NoPen)
            painter.setBrush(bg)
            radius = 6
            painter.drawRoundedRect(rect, radius, radius)

            # Draw text (white, bold)
            pen = QPen(QColor("#FFFFFF"))
            painter.setPen(pen)
            font = option.font
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.button_text)
            painter.restore()
            return
        
        # For other columns, use default painting
        super().paint(painter, option, index)
    
    def editorEvent(self, event, model, option, index):
        """Handle mouse events on the button."""
        if index.column() == 3:  # Actions column
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    # Check if click is within button bounds
                    button_rect = option.rect.adjusted(4, 4, -4, -4)
                    if button_rect.contains(event.pos()):
                        self.button_clicked.emit(index.row())
                        return True
        return super().editorEvent(event, model, option, index)
    
    def sizeHint(self, option, index):
        """Return the size hint for the button."""
        if index.column() == 3:  # Actions column
            # Make the CTA a bit larger for visibility
            font = option.font
            font.setBold(True)
            metrics = QFontMetrics(font)
            text_size = metrics.size(Qt.TextSingleLine, self.button_text)
            # Add generous padding for tap targets
            return text_size + QSize(28, 12)  # wider and taller
        return super().sizeHint(option, index)


class CourseTableModel(QAbstractTableModel):
    """Table model for displaying courses."""
    
    def __init__(self, courses: List[Course] = None):
        super().__init__()
        self.courses = courses or []
        # Remove Provider and Tags columns
        self.headers = [
            tr("table_headers.title"),
            tr("table_headers.category"),
            tr("table_headers.subcategory"),
            tr("table_headers.actions"),
        ]
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.courses)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.headers)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        
        course = self.courses[index.row()]
        col = index.column()
        
        # Get current language for multilingual data
        current_language = "en"
        try:
            from core.translations import get_translation_manager
            translation_manager = get_translation_manager()
            if translation_manager:
                current_language = translation_manager.get_current_language()
        except:
            pass
        
        if role == Qt.DisplayRole:
            if col == 0:  # Title
                return course.get_title(current_language)
            elif col == 1:  # Category
                return course.category
            elif col == 2:  # Subcategory
                return course.subcategory
            elif col == 3:  # Actions
                return ""  # Empty text, button delegate will handle display
        elif role == Qt.ToolTipRole:
            # Provide helpful tooltip on the action column
            if col == 3:
                return tr("menu_copy_link")
        
        return None
    
    def flags(self, index: QModelIndex):
        """Return item flags."""
        if not index.isValid():
            return Qt.NoItemFlags
        
        # Make the Get Link column clickable
        if index.column() == 3:  # Actions column
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
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
        self._setup_context_menu()
        self._setup_keyboard_shortcuts()
        self._setup_feedback_timer()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Apply modern styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #333333;
            }
            
            QLabel {
                color: #333333;
                font-size: 13px;
                font-weight: 500;
            }
            
            QTableView {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                gridline-color: #E5E5E7;
                selection-background-color: #E3F2FD;
                alternate-background-color: #F8F9FA;
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
                background-color: #F8F9FA;
                color: #333333;
                border: none;
                border-bottom: 1px solid #D1D1D6;
                border-right: 1px solid #E5E5E7;
                padding: 12px 8px;
                font-weight: 600;
                font-size: 13px;
            }
            
            QHeaderView::section:hover {
                background-color: #E8F4FD;
            }
            
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 500;
                min-height: 20px;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: #0056CC;
            }
            
            QPushButton:pressed {
                background-color: #004499;
            }

            /* Ultra-thin translucent scrollbars for table */
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.25);
                min-height: 40px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.35);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
                height: 0px;
            }

            QScrollBar:horizontal {
                background: transparent;
                height: 6px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 0, 0, 0.25);
                min-width: 40px;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 0, 0, 0.35);
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: transparent;
                width: 0px;
            }
        """)
        
        # Results header
        header_layout = QHBoxLayout()
        self.results_label = QLabel("Results: 0 courses")
        header_layout.addWidget(self.results_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Table view
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        
        # Enable multi-selection for "Open Selected" functionality
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # Set up the model
        self.model = CourseTableModel()
        self.table_view.setModel(self.model)
        
        # Set up button delegate for Actions column
        self.button_delegate = ButtonDelegate(self)
        self.table_view.setItemDelegateForColumn(3, self.button_delegate)
        self.button_delegate.button_clicked.connect(self._on_button_clicked)
        
        # Configure columns
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title - stretches to fill space
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Subcategory
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Actions
        
        # Set minimum widths for better UX
        header.setMinimumSectionSize(80)
        
        # Enable sorting by clicking headers
        header.setSortIndicatorShown(True)
        
        # Connect signals
        self.table_view.doubleClicked.connect(self._on_double_clicked)
        self.table_view.clicked.connect(self._on_cell_clicked)
        self.table_view.customContextMenuRequested.connect(self._show_context_menu)
        
        # Enable context menu
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        
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
    
    def _setup_context_menu(self):
        """Setup context menu for table rows."""
        self.context_menu = QMenu(self)
        
        # Copy Link action
        self.copy_action = QAction("Copy Link", self)
        self.copy_action.setShortcut(QKeySequence.Copy)
        self.copy_action.triggered.connect(self._copy_selected_link)
        self.context_menu.addAction(self.copy_action)
        
        # Open Link action
        self.open_action = QAction("Open Link in Browser", self)
        self.open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_action.triggered.connect(self._open_selected_link)
        self.context_menu.addAction(self.open_action)
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Ctrl+C for copy
        copy_shortcut = QAction(self)
        copy_shortcut.setShortcut(QKeySequence.Copy)
        copy_shortcut.triggered.connect(self._copy_selected_link)
        self.addAction(copy_shortcut)
        
        # Ctrl+O for open
        open_shortcut = QAction(self)
        open_shortcut.setShortcut(QKeySequence("Ctrl+O"))
        open_shortcut.triggered.connect(self._open_selected_link)
        self.addAction(open_shortcut)
    
    def _setup_feedback_timer(self):
        """Setup timer for user feedback messages."""
        self.feedback_timer = QTimer()
        self.feedback_timer.setSingleShot(True)
        self.feedback_timer.timeout.connect(self._hide_feedback)
        self.feedback_message = None
    
    def _on_button_clicked(self, row: int):
        """Handle button click in Actions column."""
        course = self.model.get_course(row)
        if course:
            self._copy_course_link(course)
    
    def _on_cell_clicked(self, index: QModelIndex):
        """Handle cell click - if it's the Get Link column, copy the link."""
        if index.column() == 3:  # Actions column
            course = self.model.get_course(index.row())
            if course:
                self._copy_course_link(course)
    
    def _on_double_clicked(self, index: QModelIndex):
        """Handle double-click on table row."""
        course = self.model.get_course(index.row())
        if course:
            self._copy_course_link(course)
    
    def _show_context_menu(self, position):
        """Show context menu at the given position."""
        index = self.table_view.indexAt(position)
        if index.isValid():
            course = self.model.get_course(index.row())
            if course:
                # Update action text with course title
                self.copy_action.setText(f"Copy Link: {course.title[:30]}...")
                self.open_action.setText(f"Open Link: {course.title[:30]}...")
                
                # Show context menu
                self.context_menu.exec_(self.table_view.mapToGlobal(position))
    
    def _copy_selected_link(self):
        """Copy link of the currently selected row."""
        selection = self.table_view.selectionModel()
        if selection and selection.hasSelection():
            index = selection.currentIndex()
            course = self.model.get_course(index.row())
            if course:
                self._copy_course_link(course)
    
    def _open_selected_link(self):
        """Open link of the currently selected row in browser."""
        selection = self.table_view.selectionModel()
        if selection and selection.hasSelection():
            index = selection.currentIndex()
            course = self.model.get_course(index.row())
            if course:
                self._open_course_link(course)
    
    def _copy_course_link(self, course: Course):
        """Copy a course link to clipboard with feedback."""
        if self._copy_to_clipboard(course.link):
            self._show_feedback(f"Copied: {course.title[:30]}...")
            self.course_link_requested.emit(course)
        else:
            self._show_feedback("Failed to copy link", is_error=True)
    
    def _open_course_link(self, course: Course):
        """Open a course link in browser with feedback."""
        try:
            webbrowser.open(course.link)
            self._show_feedback(f"Opened: {course.title[:30]}...")
            self.course_open_requested.emit(course)
        except Exception as e:
            self._show_feedback(f"Failed to open link: {str(e)}", is_error=True)
    
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
    
    def _show_feedback(self, message: str, is_error: bool = False):
        """Show non-blocking feedback message."""
        # Hide previous message
        self._hide_feedback()
        
        # Show tooltip as feedback
        pos = self.mapToGlobal(self.rect().bottomLeft())
        QToolTip.showText(pos, message, self, self.rect(), 3000)  # 3 second timeout
        
        # Also update status if available
        if hasattr(self.parent(), 'statusBar'):
            self.parent().statusBar().showMessage(message, 3000)
    
    def _hide_feedback(self):
        """Hide feedback message."""
        QToolTip.hideText()
