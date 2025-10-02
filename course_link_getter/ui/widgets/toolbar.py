from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon


class Toolbar(QWidget):
    """Toolbar with action buttons for course operations."""
    
    # Signals
    show_all_clicked = pyqtSignal()
    export_csv_clicked = pyqtSignal()
    copy_links_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Show all button
        self.show_all_btn = QPushButton("Show All Results")
        self.show_all_btn.clicked.connect(self.show_all_clicked.emit)
        layout.addWidget(self.show_all_btn)
        
        # Export CSV button
        self.export_csv_btn = QPushButton("Export to CSV")
        self.export_csv_btn.clicked.connect(self.export_csv_clicked.emit)
        layout.addWidget(self.export_csv_btn)
        
        # Copy links button
        self.copy_links_btn = QPushButton("Copy All Links")
        self.copy_links_btn.clicked.connect(self.copy_links_clicked.emit)
        layout.addWidget(self.copy_links_btn)
        
        # Add spacer to push buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
    
    def set_status(self, message: str):
        """Set the status message."""
        self.status_label.setText(message)
    
    def set_export_enabled(self, enabled: bool):
        """Enable/disable export button."""
        self.export_csv_btn.setEnabled(enabled)
    
    def set_copy_links_enabled(self, enabled: bool):
        """Enable/disable copy links button."""
        self.copy_links_btn.setEnabled(enabled)
