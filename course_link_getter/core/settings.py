"""
Settings management for Course Link Getter.

Handles persistence of user preferences and filter states.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from platformdirs import user_data_dir


class SettingsManager:
    """Manages application settings and persistence."""
    
    def __init__(self, app_name: str = "CourseLinkGetter"):
        """Initialize settings manager."""
        self.app_name = app_name
        self.settings_dir = Path(user_data_dir(app_name, "CourseLinkGetter"))
        self.settings_file = self.settings_dir / "settings.json"
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Failed to load settings: {e}")
        
        # Return default settings
        return {
            "filters": {
                "category": None,
                "subcategory": None,
                "search_text": ""
            },
            "window": {
                "width": 1200,
                "height": 800
            }
        }
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            # Ensure settings directory exists
            self.settings_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Failed to save settings: {e}")
    
    def get_filter_settings(self) -> Dict[str, Optional[str]]:
        """Get current filter settings."""
        return self.settings.get("filters", {
            "category": None,
            "subcategory": None,
            "search_text": ""
        })
    
    def set_filter_settings(self, category: Optional[str] = None, 
                          subcategory: Optional[str] = None, 
                          search_text: str = ""):
        """Set filter settings."""
        if "filters" not in self.settings:
            self.settings["filters"] = {}
        
        if category is not None:
            self.settings["filters"]["category"] = category
        if subcategory is not None:
            self.settings["filters"]["subcategory"] = subcategory
        if search_text is not None:
            self.settings["filters"]["search_text"] = search_text
        
        self._save_settings()
    
    def get_window_settings(self) -> Dict[str, int]:
        """Get window settings."""
        return self.settings.get("window", {
            "width": 1200,
            "height": 800
        })
    
    def set_window_settings(self, width: int, height: int):
        """Set window settings."""
        if "window" not in self.settings:
            self.settings["window"] = {}
        
        self.settings["window"]["width"] = width
        self.settings["window"]["height"] = height
        self._save_settings()
    
    def clear_filter_settings(self):
        """Clear all filter settings."""
        self.settings["filters"] = {
            "category": None,
            "subcategory": None,
            "search_text": ""
        }
        self._save_settings()
