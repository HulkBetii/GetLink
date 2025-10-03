from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QMessageBox, QFileDialog, QApplication,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableView,
    QAbstractItemView, QHeaderView, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence, QFont
from typing import List
import sys
import subprocess
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from .widgets.results_view import CourseTableModel, ButtonDelegate
from .widgets.language_selector import LanguageSelector
from .widgets.rtl_helper import RTLHelper
from core.store import CatalogStore
from core.models import Course
from core.settings import SettingsManager
from core.translations import init_translations, get_translation_manager, tr


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PyQt5.QtGui import QGuiApplication, QCursor

class NotificationWidget(QWidget):
    """Custom notification widget for showing copy success messages."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool  # tránh hiện trên task switcher một số nền tảng
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus, True)  # tránh cướp focus
        self.setFixedSize(400, 80)

        # --- UI ---
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
                border-radius: 12px;
                border: 2px solid #45a049;
            }
        """)

        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 10)

        self.icon_label = QLabel("✓")
        self.icon_label.setStyleSheet("""
            QLabel { color: white; font-size: 24px; font-weight: bold; }
        """)
        layout.addWidget(self.icon_label)

        self.message_label = QLabel(tr("status_copied"))
        self.message_label.setStyleSheet("""
            QLabel { color: white; font-size: 16px; font-weight: 600; }
        """)
        layout.addWidget(self.message_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        # --- Effects & Animations ---
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InCubic)
        # kết nối 1 lần để tránh trùng lặp
        self.fade_out_animation.finished.connect(self.hide)

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_notification)

        self.opacity_effect.setOpacity(0.0)
        self.hide()

    # ---------- ĐẶT VỊ TRÍ GÓC TRÊN-PHẢI ----------

    def _screen_for_widget(self):
        """Chọn màn hình hợp lý: chứa parent (global), hoặc con trỏ, hoặc màn hình chính."""
        parent = self.parent() if isinstance(self.parent(), QWidget) else None

        # Ưu tiên: màn hình nơi đặt parent (global center)
        if parent:
            center_global = parent.mapToGlobal(QPoint(parent.width() // 2, parent.height() // 2))
            scr = QGuiApplication.screenAt(center_global)
            if scr:
                return scr

        # Fallback: màn hình dưới con trỏ
        scr = QGuiApplication.screenAt(QCursor.pos())
        if scr:
            return scr

        # Cuối cùng: màn hình chính
        return QGuiApplication.primaryScreen()

    def _place_top_right_on_screen(self, margin=16):
        """Đặt toast ở góc trên-phải của màn hình (tôn trọng taskbar/dock)."""
        screen = self._screen_for_widget()
        arect = screen.availableGeometry()  # không đè lên taskbar/dock

        # Clamp kích thước nếu toast lớn hơn vùng khả dụng
        w = min(self.width(), arect.width())
        h = min(self.height(), arect.height())

        # Tính toạ độ: góc trên-phải, có margin
        x = arect.right() - w - margin
        y = arect.top() + margin

        # Đề phòng DPI/khung: ép trong biên
        x = max(arect.left(), x)
        y = max(arect.top(), y)

        # Nếu có thay đổi kích thước do clamp, áp dụng tạm thời
        if (w, h) != (self.width(), self.height()):
            self.resize(w, h)
        self.move(x, y)

    def _place_top_right_in_parent(self, margin=16):
        """Đặt toast bám theo cửa sổ cha (góc trên-phải parent)."""
        parent = self.parent()
        if not isinstance(parent, QWidget):
            return False

        # Check if current language is RTL
        is_rtl = False
        try:
            from core.translations import get_translation_manager
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
        except:
            pass

        if is_rtl:
            # For RTL languages, position at top-left
            top_left_global = parent.mapToGlobal(QPoint(0, 0))
            x = top_left_global.x() + margin
            y = top_left_global.y() + margin
        else:
            # For LTR languages, position at top-right
            top_right_global = parent.mapToGlobal(QPoint(parent.width(), 0))
            x = top_right_global.x() - self.width() - margin
            y = top_right_global.y() + margin

        # Clamp trong vùng màn hình chứa parent
        screen = QGuiApplication.screenAt(QPoint(x, y)) or QGuiApplication.primaryScreen()
        arect = screen.availableGeometry()
        x = max(arect.left(), min(x, arect.right() - self.width()))
        y = max(arect.top(),  min(y, arect.bottom() - self.height()))

        self.move(x, y)
        return True

    # ---------- HIỂN THỊ / ẨN ----------

    def show_notification(self, message=None, pin_to_parent=True, duration_ms=4000):
        """Hiển thị thông báo ở góc trên-phải, bảo đảm không tràn màn hình."""
        if message is None:
            message = tr("status_copied")
        self.message_label.setText(message)
        
        # Apply RTL support to notification
        if hasattr(self, 'parent') and self.parent():
            from core.translations import get_translation_manager
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
                RTLHelper.apply_rtl_layout(self, is_rtl)

        placed = False
        if pin_to_parent:
            placed = self._place_top_right_in_parent(margin=16)
        if not placed:
            self._place_top_right_on_screen(margin=16)

        # Không cướp focus
        # self.activateWindow()  # bỏ dòng này

        self.opacity_effect.setOpacity(0.0)
        self.show()
        self.raise_()
        self.fade_in_animation.start()
        self.hide_timer.start(duration_ms)

    def hide_notification(self):
        """Ẩn với fade-out (đã connect self.hide 1 lần trong __init__)."""
        self.fade_out_animation.start()



class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.store = CatalogStore()
        self.settings_manager = SettingsManager()
        self.current_courses: List[Course] = []
        
        # Disable translations
        self.translation_manager = init_translations(QApplication.instance())
        
        # Load data first before setting up UI
        self._load_initial_data()
        self._setup_ui()
        self._connect_signals()
        
        # Create notification widget
        self.notification = NotificationWidget(self)
        
        # Connect window events to reposition notification
        self.moveEvent = self._on_window_move
        self.resizeEvent = self._on_window_resize
        
        # Multilingual disabled: skip saved language
    
    def _load_saved_language(self):
        """Load saved language from settings or detect system language."""
        saved_language = self.settings_manager.get_language_code()
        
        # If no saved language, detect system language
        if saved_language == "en" and self.translation_manager:
            detected_language = self.translation_manager.detect_system_language()
            if detected_language != "en":
                saved_language = detected_language
                self.settings_manager.set_language_settings(saved_language)
        
        if self.translation_manager:
            self.translation_manager.load_language(saved_language)
            self.language_selector.set_language(saved_language)
    
    def _on_language_changed(self, language_code: str):
        """Handle language change."""
        if self.translation_manager:
            self.translation_manager.load_language(language_code)
            self.settings_manager.set_language_settings(language_code)
            
            # Apply RTL support if needed
            self._apply_rtl_support()
            
            # Reload data with new language
            self._load_initial_data()
            
            # Update UI text
            self._update_ui_text()
            
            # Refresh the display
            self._on_filters_changed()
    
    def _update_ui_text(self):
        """Update all UI text with current translations."""
        # Update search placeholder
        self.search_input.setPlaceholderText(tr("search_placeholder"))
        
        # Update combo boxes
        self.category_combo.setItemText(0, tr("category_all"))
        self.subcategory_combo.setItemText(0, tr("subcategory_all"))
        
        # Update buttons
        self.show_all_btn.setText(tr("show_all"))
        self.copy_links_btn.setText(tr("copy_links"))
        self.export_csv_btn.setText(tr("export_csv"))
        
        # Update table headers (4 columns only)
        self.model.headers = [
            tr("table_headers.title"),
            tr("table_headers.category"),
            tr("table_headers.subcategory"),
            tr("table_headers.actions"),
        ]
        self.model.headerDataChanged.emit(Qt.Horizontal, 0, len(self.model.headers) - 1)
        
        # Update button delegate text
        self.button_delegate.button_text = tr("get_link")
        
        # Update status
        self.statusBar().showMessage(tr("status_ready"))
    
    def _apply_rtl_support(self):
        """Apply RTL support to the entire application."""
        if not self.translation_manager:
            return
        
        is_rtl = self.translation_manager.is_rtl_language(self.translation_manager.get_current_language())
        
        # Apply RTL layout direction to main window
        RTLHelper.apply_rtl_layout(self, is_rtl)
        
        # Apply RTL styles
        rtl_styles = RTLHelper.get_rtl_style_adjustments(is_rtl)
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + rtl_styles)
        
        # Apply RTL to all child widgets
        self._apply_rtl_to_children(self, is_rtl)
    
    def _apply_rtl_to_children(self, widget, is_rtl: bool):
        """Recursively apply RTL support to child widgets."""
        for child in widget.findChildren(QWidget):
            RTLHelper.apply_rtl_layout(child, is_rtl)
    
    def _on_window_move(self, event):
        """Handle window move event to reposition notification."""
        if hasattr(self, 'notification') and self.notification.isVisible():
            # Reposition notification when window moves
            parent_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.notification.width()) // 2
            y = parent_rect.y() + 50
            self.notification.move(x, y)
        super().moveEvent(event)
    
    def _on_window_resize(self, event):
        """Handle window resize event to reposition notification."""
        if hasattr(self, 'notification') and self.notification.isVisible():
            # Reposition notification when window resizes
            parent_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.notification.width()) // 2
            y = parent_rect.y() + 50
            self.notification.move(x, y)
        # Keep results table column proportions on resize
        if hasattr(self, 'table_view'):
            self._apply_results_column_layout()
        super().resizeEvent(event)

    def _apply_results_column_layout(self):
        """Divide width: Title = 1/2; remaining 1/2 split into 5 parts where
        Category = 2 parts, Subcategory = 2 parts, Actions = 1 part.
        Resulting ratios: Title 50%, Category 20%, Subcategory 20%, Actions 10%.
        """
        try:
            if not hasattr(self, 'table_view') or self.table_view is None:
                return
            viewport_width = self.table_view.viewport().width()
            if viewport_width <= 0:
                return
            total = viewport_width
            title_w = max(0, total // 2)
            remaining = max(0, total - title_w)
            if remaining <= 0:
                # Fallback: make title occupy all
                self.table_view.setColumnWidth(0, total)
                return
            unit = remaining // 5
            category_w = unit * 2
            subcat_w = unit * 2
            actions_w = remaining - category_w - subcat_w
            self.table_view.setColumnWidth(0, title_w)
            self.table_view.setColumnWidth(1, category_w)
            self.table_view.setColumnWidth(2, subcat_w)
            self.table_view.setColumnWidth(3, actions_w)
        except Exception:
            pass
    
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
        
        # Filter and action panel (horizontal)
        self._create_filter_panel(main_layout)
        
        # Results section
        self._create_results_section(main_layout)
        
        # Menu bar
        self._create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    
    def _create_filter_panel(self, parent_layout):
        """Create the horizontal filter and action panel."""
        filter_widget = QWidget()
        filter_widget.setFixedHeight(120)  # Increased height for two rows
        filter_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-bottom: 1px solid #E5E5E5;
            }
        """)
        
        # Main vertical layout
        main_layout = QVBoxLayout(filter_widget)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)
        
        # Row 1: Search and Categories
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(15)
        
        # Search section
        search_label = QLabel("Search:")
        search_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        row1_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr("search_placeholder"))
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
        row1_layout.addWidget(self.search_input)
        
        # Category section
        category_label = QLabel("Category:")
        category_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        row1_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItem(tr("category_all"))
        self.category_combo.setFixedWidth(150)
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:hover {
                border-color: #007AFF;
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
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                selection-background-color: #E3F2FD;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F5F5F5;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
        row1_layout.addWidget(self.category_combo)
        
        # Subcategory section
        subcategory_label = QLabel("Subcategory:")
        subcategory_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #333333;
                font-size: 13px;
            }
        """)
        row1_layout.addWidget(subcategory_label)
        
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.addItem(tr("subcategory_all"))
        self.subcategory_combo.setFixedWidth(150)
        self.subcategory_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:hover {
                border-color: #007AFF;
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
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                selection-background-color: #E3F2FD;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F5F5F5;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
        row1_layout.addWidget(self.subcategory_combo)
        
        # Add spacer to push everything to the left
        row1_layout.addStretch()
        
        # Row 2: Language selector and Action buttons
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(15)
        
        # Language selector (disabled)
        spacer = QWidget()
        spacer.setFixedWidth(1)
        row2_layout.addWidget(spacer)
        
        # Add spacer
        row2_layout.addStretch()
        
        # Action buttons
        self.show_all_btn = QPushButton(tr("show_all"))
        self.show_all_btn.setFixedHeight(35)
        self.show_all_btn.setMinimumWidth(80)
        self.show_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        row2_layout.addWidget(self.show_all_btn)
        
        self.copy_links_btn = QPushButton(tr("copy_links"))
        self.copy_links_btn.setFixedHeight(35)
        self.copy_links_btn.setMinimumWidth(100)
        self.copy_links_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        row2_layout.addWidget(self.copy_links_btn)
        
        self.export_csv_btn = QPushButton(tr("export_csv"))
        self.export_csv_btn.setFixedHeight(35)
        self.export_csv_btn.setMinimumWidth(80)
        self.export_csv_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        row2_layout.addWidget(self.export_csv_btn)
        
        # Add both rows to main layout
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        
        # Apply RTL support to filter widget
        if self.translation_manager:
            is_rtl = self.translation_manager.is_rtl_language(self.translation_manager.get_current_language())
            RTLHelper.apply_rtl_layout(filter_widget, is_rtl)
        
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

            /* Ultra-thin translucent scrollbars */
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
        
        # Set up the model
        self.model = CourseTableModel()
        self.table_view.setModel(self.model)
        
        # Set up button delegate for Actions column
        self.button_delegate = ButtonDelegate(self)
        # Actions column index is 3 after removing Provider/Tags
        self.table_view.setItemDelegateForColumn(3, self.button_delegate)
        self.button_delegate.button_clicked.connect(self._on_button_clicked)
        
        # Configure columns
        header = self.table_view.horizontalHeader()
        # Use interactive sizing and maintain proportions manually
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Title
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Category
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Subcategory
        header.setSectionResizeMode(3, QHeaderView.Interactive)  # Action
        
        # Enable sorting and selection
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        results_layout.addWidget(self.table_view)
        
        # Apply initial proportional layout after the view is shown
        QTimer.singleShot(0, self._apply_results_column_layout)
        
        # Apply RTL support to results widget
        if self.translation_manager:
            is_rtl = self.translation_manager.is_rtl_language(self.translation_manager.get_current_language())
            RTLHelper.apply_rtl_layout(results_widget, is_rtl)
        
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
    
    def _on_button_clicked(self, row: int):
        """Handle button click in Actions column."""
        course = self.model.get_course(row)
        if course:
            self._copy_course_link(course)
    
    def _on_table_clicked(self, index):
        """Handle table cell click."""
        if index.column() == 5:  # Action column
            course = self.model.get_course(index.row())
            if course:
                self._copy_course_link(course)
    
    def _load_initial_data(self):
        """Load initial data from legacy single-language catalog only."""
        legacy_path = Path(__file__).parent.parent / "assets" / "catalog.sample.json"
        if legacy_path.exists():
            if self.store.load_from_json(str(legacy_path)):
                print(f"✅ Loaded {len(self.store.list_all())} courses from legacy catalog")
                return True
        print("❌ Failed to load catalog data")
        return False
    
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
            # Show popup notification
            self.notification.show_notification(f"✓ Copied: {course.title[:30]}...")
            # Also update status bar
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
            # Show popup notification
            self.notification.show_notification(f"✓ Copied {len(links)} links to clipboard")
            # Also update status bar
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
                # Export only the specified columns: title, category, subcategory, link
                fieldnames = ['title', 'category', 'subcategory', 'link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in self.current_courses:
                    writer.writerow({
                        'title': course.title,
                        'category': course.category,
                        'subcategory': course.subcategory,
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
