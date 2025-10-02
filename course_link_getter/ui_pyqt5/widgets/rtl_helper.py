"""
RTL (Right-to-Left) support helper for UI components.
"""

from PyQt5.QtWidgets import QWidget, QLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from typing import Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.translations import get_translation_manager


class RTLHelper:
    """Helper class for RTL language support."""
    
    @staticmethod
    def apply_rtl_layout(widget: QWidget, is_rtl: bool = None):
        """Apply RTL layout direction to a widget."""
        if is_rtl is None:
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
            else:
                is_rtl = False
        
        if is_rtl:
            widget.setLayoutDirection(Qt.RightToLeft)
        else:
            widget.setLayoutDirection(Qt.LeftToRight)
    
    @staticmethod
    def get_rtl_style_adjustments(is_rtl: bool = None) -> str:
        """Get CSS style adjustments for RTL languages."""
        if is_rtl is None:
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
            else:
                is_rtl = False
        
        if is_rtl:
            return """
                QWidget {
                    direction: rtl;
                }
                QLineEdit {
                    text-align: right;
                }
                QComboBox {
                    text-align: right;
                }
                QLabel {
                    text-align: right;
                }
                QPushButton {
                    text-align: center;
                }
                QTableView {
                    text-align: right;
                }
                QHeaderView::section {
                    text-align: right;
                }
            """
        else:
            return """
                QWidget {
                    direction: ltr;
                }
                QLineEdit {
                    text-align: left;
                }
                QComboBox {
                    text-align: left;
                }
                QLabel {
                    text-align: left;
                }
                QPushButton {
                    text-align: center;
                }
                QTableView {
                    text-align: left;
                }
                QHeaderView::section {
                    text-align: left;
                }
            """
    
    @staticmethod
    def reverse_layout_items(layout: QLayout, is_rtl: bool = None):
        """Reverse the order of items in a layout for RTL languages."""
        if is_rtl is None:
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
            else:
                is_rtl = False
        
        if is_rtl and layout:
            # Get all items
            items = []
            while layout.count():
                item = layout.takeAt(0)
                if item:
                    items.append(item)
            
            # Add them back in reverse order
            for item in reversed(items):
                if isinstance(layout, QHBoxLayout):
                    layout.addItem(item)
                elif isinstance(layout, QVBoxLayout):
                    layout.addItem(item)
    
    @staticmethod
    def get_margin_adjustments(is_rtl: bool = None) -> dict:
        """Get margin adjustments for RTL layouts."""
        if is_rtl is None:
            translation_manager = get_translation_manager()
            if translation_manager:
                is_rtl = translation_manager.is_rtl_language(translation_manager.get_current_language())
            else:
                is_rtl = False
        
        if is_rtl:
            return {
                'left_margin': 0,
                'right_margin': 20,
                'text_align': 'right'
            }
        else:
            return {
                'left_margin': 20,
                'right_margin': 0,
                'text_align': 'left'
            }
    
    @staticmethod
    def is_current_language_rtl() -> bool:
        """Check if current language is RTL."""
        translation_manager = get_translation_manager()
        if translation_manager:
            return translation_manager.is_rtl_language(translation_manager.get_current_language())
        return False


class RTLWidget(QWidget):
    """Base widget class with automatic RTL support."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_rtl_support()
    
    def _apply_rtl_support(self):
        """Apply RTL support to this widget."""
        RTLHelper.apply_rtl_layout(self, RTLHelper.is_current_language_rtl())
        
        # Apply RTL styles
        rtl_styles = RTLHelper.get_rtl_style_adjustments(RTLHelper.is_current_language_rtl())
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + rtl_styles)
    
    def update_rtl_layout(self):
        """Update RTL layout when language changes."""
        self._apply_rtl_support()
        self.update()
