from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QLineEdit, QGroupBox
)
from PyQt6.QtCore import pyqtSignal
from typing import List, Optional
from ...core.models import Category


class FiltersPanel(QWidget):
    """Panel for category and subcategory filtering controls."""
    
    # Signals
    category_changed = pyqtSignal(str)
    subcategory_changed = pyqtSignal(str)
    search_changed = pyqtSignal(str)
    show_all_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.categories: List[Category] = []
        self.current_category: Optional[str] = None
        self.current_subcategory: Optional[str] = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
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
        
        # Show all button
        self.show_all_btn = QPushButton("Show All Results")
        self.show_all_btn.clicked.connect(self.show_all_clicked.emit)
        layout.addWidget(self.show_all_btn)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def set_categories(self, categories: List[Category]):
        """Set the available categories."""
        self.categories = categories
        self._update_category_combo()
    
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
        else:
            self.current_category = category_name
            # Find the selected category and update subcategories
            for category in self.categories:
                if category.name == category_name:
                    self._update_subcategory_combo(category.subcategories)
                    break
        
        self.category_changed.emit(category_name)
    
    def _on_subcategory_changed(self, subcategory_name: str):
        """Handle subcategory selection change."""
        if subcategory_name == "All Subcategories":
            self.current_subcategory = None
        else:
            self.current_subcategory = subcategory_name
        
        self.subcategory_changed.emit(subcategory_name)
    
    def _on_search_changed(self, text: str):
        """Handle search text change."""
        self.search_changed.emit(text)
    
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
    
    def clear_filters(self):
        """Clear all filters."""
        self.search_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.subcategory_combo.setCurrentIndex(0)
        self.current_category = None
        self.current_subcategory = None
