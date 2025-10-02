from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QLineEdit, QGroupBox
)
from PyQt5.QtCore import pyqtSignal, QTimer
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.models import Category
from core.store import CatalogStore
from core.settings import SettingsManager


class FiltersPanel(QWidget):
    """Panel for category and subcategory filtering controls."""
    
    # Signals
    filters_changed = pyqtSignal()  # Emitted when any filter changes
    
    def __init__(self, store: CatalogStore, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.store = store
        self.settings_manager = settings_manager
        self.categories: List[Category] = []
        self.current_category: Optional[str] = None
        self.current_subcategory: Optional[str] = None
        
        # Search debounce timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._on_search_timeout)
        
        self._setup_ui()
        self._load_categories()
        self._restore_settings()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Apply modern styling
        self.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                color: #333333;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #FAFAFA;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background-color: #FAFAFA;
                color: #333333;
            }
            
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 24px;
                font-size: 13px;
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
                width: 24px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 8px;
            }
            
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 10px 12px;
                min-height: 24px;
                font-size: 13px;
            }
            
            QLineEdit:hover {
                border-color: #007AFF;
            }
            
            QLineEdit:focus {
                border-color: #007AFF;
                outline: none;
            }
            
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                min-height: 24px;
                font-size: 13px;
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
            
            QLabel {
                color: #333333;
                font-size: 13px;
            }
        """)
        
        # Search box
        search_group = QGroupBox("Search")
        search_layout = QVBoxLayout(search_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_group)
        
        # Category selection
        category_group = QGroupBox("Category")
        category_layout = QVBoxLayout(category_group)
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories", None)
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        category_layout.addWidget(self.category_combo)
        
        layout.addWidget(category_group)
        
        # Subcategory selection
        subcategory_group = QGroupBox("Subcategory")
        subcategory_layout = QVBoxLayout(subcategory_group)
        
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.addItem("All Subcategories", None)
        self.subcategory_combo.currentTextChanged.connect(self._on_subcategory_changed)
        subcategory_layout.addWidget(self.subcategory_combo)
        
        layout.addWidget(subcategory_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.show_all_btn = QPushButton("Show All Results")
        self.show_all_btn.clicked.connect(self._show_all_courses)
        button_layout.addWidget(self.show_all_btn)
        
        self.clear_filters_btn = QPushButton("Clear Filters")
        self.clear_filters_btn.clicked.connect(self._clear_filters)
        button_layout.addWidget(self.clear_filters_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def _load_categories(self):
        """Load categories from store on app launch."""
        self.categories = self.store.list_categories()
        self._update_category_combo()
        self._update_subcategory_combo([])  # Start with disabled subcategory
    
    def _update_category_combo(self):
        """Update the category combo box with available categories."""
        self.category_combo.clear()
        self.category_combo.addItem("All Categories", None)
        
        for category in self.categories:
            self.category_combo.addItem(category.name, category.name)
    
    def _on_category_changed(self, category_name: str):
        """Handle category selection change."""
        if category_name == "All Categories":
            self.current_category = None
            self._update_subcategory_combo([])
            self.subcategory_combo.setEnabled(False)
        else:
            self.current_category = category_name
            # Find the selected category and update subcategories
            for category in self.categories:
                if category.name == category_name:
                    self._update_subcategory_combo(category.subcategories)
                    self.subcategory_combo.setEnabled(True)
                    break
        
        self._apply_filters()
    
    def _on_subcategory_changed(self, subcategory_name: str):
        """Handle subcategory selection change."""
        if subcategory_name == "All Subcategories":
            self.current_subcategory = None
        else:
            self.current_subcategory = subcategory_name
        
        self._apply_filters()
    
    def _on_search_changed(self, text: str):
        """Handle search text change with debouncing."""
        # Restart the timer for debounced search
        self.search_timer.stop()
        self.search_timer.start(100)  # 100ms delay
    
    def _on_search_timeout(self):
        """Handle search timeout (debounced search)."""
        self._apply_filters()
    
    def _apply_filters(self):
        """Apply current filters and emit change signal."""
        self._save_current_settings()
        self.filters_changed.emit()
    
    def _restore_settings(self):
        """Restore filter settings from saved preferences."""
        settings = self.settings_manager.get_filter_settings()
        
        # Restore category
        if settings.get("category"):
            category_name = settings["category"]
            for i in range(self.category_combo.count()):
                if self.category_combo.itemText(i) == category_name:
                    self.category_combo.setCurrentIndex(i)
                    self._on_category_changed(category_name)
                    break
        
        # Restore subcategory (only if category is set)
        if settings.get("subcategory") and self.current_category:
            subcategory_name = settings["subcategory"]
            for i in range(self.subcategory_combo.count()):
                if self.subcategory_combo.itemText(i) == subcategory_name:
                    self.subcategory_combo.setCurrentIndex(i)
                    self._on_subcategory_changed(subcategory_name)
                    break
        
        # Restore search text
        if settings.get("search_text"):
            self.search_input.setText(settings["search_text"])
    
    def _save_current_settings(self):
        """Save current filter settings."""
        self.settings_manager.set_filter_settings(
            category=self.current_category,
            subcategory=self.current_subcategory,
            search_text=self.search_input.text().strip()
        )
    
    def _show_all_courses(self):
        """Show all courses without filters."""
        self._clear_filters()
    
    def _clear_filters(self):
        """Clear all filters and reset controls."""
        self.search_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.subcategory_combo.setCurrentIndex(0)
        self.subcategory_combo.setEnabled(False)
        self.current_category = None
        self.current_subcategory = None
        self.settings_manager.clear_filter_settings()
        self._apply_filters()
    
    def _update_subcategory_combo(self, subcategories: List[str]):
        """Update the subcategory combo box."""
        self.subcategory_combo.clear()
        self.subcategory_combo.addItem("All Subcategories", None)
        
        for subcategory in subcategories:
            self.subcategory_combo.addItem(subcategory, subcategory)
    
    def get_current_filters(self) -> dict:
        """Get current filter values."""
        return {
            'category': self.current_category,
            'subcategory': self.current_subcategory,
            'search': self.search_input.text().strip()
        }
    
    def get_filtered_courses(self):
        """Get filtered courses from store."""
        filters = self.get_current_filters()
        return self.store.filter(
            category=filters['category'],
            subcategory=filters['subcategory'],
            text=filters['search'] if filters['search'] else None
        )
