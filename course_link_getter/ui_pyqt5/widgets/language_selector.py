"""
Language selection widget for multilingual support.
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QMenu, QAction, QActionGroup
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont
from typing import Dict, Any, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.translations import get_translation_manager
from .rtl_helper import RTLHelper


class LanguageSelector(QWidget):
    """Widget for selecting application language."""
    
    language_changed = pyqtSignal(str)  # Emits language code when changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.translation_manager = get_translation_manager()
        self.current_language = "en"
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the language selector UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Language label
        self.language_label = QLabel("🌐")
        self.language_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
            }
        """)
        layout.addWidget(self.language_label)
        
        # Language combo box
        self.language_combo = QComboBox()
        self.language_combo.setMinimumWidth(120)
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                color: #333333;
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
        
        # Populate language options
        self._populate_languages()
        
        layout.addWidget(self.language_combo)
        layout.addStretch()
    
    def _populate_languages(self):
        """Populate the language combo box with available languages."""
        if not self.translation_manager:
            return
        
        available_languages = self.translation_manager.get_available_languages()
        
        for lang_code, lang_data in available_languages.items():
            flag = lang_data.get("flag", "🌐")
            native_name = lang_data.get("language_native", lang_code)
            is_rtl = lang_data.get("rtl", False)
            
            # For RTL languages, show flag on the right
            if is_rtl:
                display_text = f"{native_name} {flag}"
            else:
                display_text = f"{flag} {native_name}"
            
            self.language_combo.addItem(display_text, lang_code)
    
    def _connect_signals(self):
        """Connect widget signals."""
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
    
    def _on_language_changed(self, text: str):
        """Handle language selection change."""
        # Get the language code from the combo box data
        current_index = self.language_combo.currentIndex()
        if current_index >= 0:
            lang_code = self.language_combo.itemData(current_index)
            if lang_code and lang_code != self.current_language:
                self.current_language = lang_code
                self.language_changed.emit(lang_code)
    
    def set_language(self, language_code: str):
        """Set the current language programmatically."""
        if not self.translation_manager:
            return
        
        # Find the index for this language code
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == language_code:
                self.language_combo.setCurrentIndex(i)
                self.current_language = language_code
                break
    
    def get_current_language(self) -> str:
        """Get the currently selected language code."""
        return self.current_language
    
    def refresh_languages(self):
        """Refresh the language list from the translation manager."""
        self.language_combo.clear()
        self._populate_languages()
        
        # Restore current selection if possible
        if self.current_language:
            self.set_language(self.current_language)
        
        # Apply RTL support
        self._apply_rtl_support()
    
    def _apply_rtl_support(self):
        """Apply RTL support to the language selector."""
        if self.translation_manager:
            is_rtl = self.translation_manager.is_rtl_language(self.translation_manager.get_current_language())
            RTLHelper.apply_rtl_layout(self, is_rtl)


class LanguageMenu(QMenu):
    """Context menu for language selection."""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.translation_manager = get_translation_manager()
        self.current_language = "en"
        self._setup_menu()
    
    def _setup_menu(self):
        """Setup the language menu."""
        self.setTitle("🌐 Language")
        
        # Create action group for radio button behavior
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        
        # Add language actions
        if self.translation_manager:
            available_languages = self.translation_manager.get_available_languages()
            
            for lang_code, lang_data in available_languages.items():
                flag = lang_data.get("flag", "🌐")
                native_name = lang_data.get("language_native", lang_code)
                display_text = f"{flag} {native_name}"
                
                action = QAction(display_text, self)
                action.setData(lang_code)
                action.setCheckable(True)
                action.triggered.connect(lambda checked, code=lang_code: self._on_language_selected(code))
                
                self.action_group.addAction(action)
                self.addAction(action)
    
    def _on_language_selected(self, language_code: str):
        """Handle language selection."""
        if language_code != self.current_language:
            self.current_language = language_code
            self.language_changed.emit(language_code)
    
    def set_current_language(self, language_code: str):
        """Set the current language and update menu state."""
        self.current_language = language_code
        
        # Update action states
        for action in self.action_group.actions():
            if action.data() == language_code:
                action.setChecked(True)
                break
