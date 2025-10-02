"""
Translation system for Course Link Getter.
Supports multiple languages with JSON-based translation files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication


class TranslationManager(QObject):
    """Manages translations and language switching."""
    
    language_changed = pyqtSignal(str)  # Emits when language changes
    
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.current_language = "en"
        self.translations = {}
        self.translator = QTranslator()
        
        # Get translations directory
        self.translations_dir = Path(__file__).parent / "translations"
        self.translations_dir.mkdir(exist_ok=True)
        
        # Load available languages
        self.available_languages = self._load_available_languages()
        
        # Load default language
        self.load_language("en")
    
    def _load_available_languages(self) -> Dict[str, Dict[str, Any]]:
        """Load all available language files."""
        languages = {}
        
        # Default English translations
        languages["en"] = {
            "language_name": "English",
            "language_native": "English",
            "flag": "🇺🇸",
            "ui": {
                "app_title": "Course Link Getter",
                "app_subtitle": "Browse and access course links through hierarchical categories",
                "search_placeholder": "Search courses...",
                "category_all": "All Categories",
                "subcategory_all": "All Subcategories",
                "show_all": "All Results",
                "export_csv": "Export CSV",
                "copy_links": "Copy Visible Links",
                "open_selected": "Open Selected",
                "results_count": "Loaded {count} courses",
                "results_filtered": "{count} results (filtered)",
                "status_ready": "Ready",
                "status_loading": "Loading...",
                "status_exporting": "Exporting...",
                "status_copied": "Copied to clipboard!",
                "status_opened": "Opened in browser",
                "status_exported": "Exported to CSV",
                "status_error": "Error occurred",
                "get_link": "Get Link",
                "copy_link": "Copy Link",
                "open_link": "Open Link in Browser",
                "table_headers": {
                    "title": "Title",
                    "category": "Category", 
                    "subcategory": "Subcategory",
                    
                    "actions": "Actions"
                },
                "menu_file": "File",
                "menu_edit": "Edit",
                "menu_view": "View",
                "menu_help": "Help",
                "menu_export": "Export to CSV...",
                "menu_exit": "Exit",
                "menu_language": "Language",
                "menu_about": "About",
                "dialog_export_title": "Export to CSV",
                "dialog_export_message": "Choose where to save the CSV file:",
                "dialog_open_selected_title": "Open Selected Courses",
                "dialog_open_selected_message": "Open {count} selected courses in browser?",
                "dialog_confirm": "Confirm",
                "dialog_cancel": "Cancel",
                "dialog_save": "Save",
                "dialog_open": "Open",
                "error_no_courses": "No courses found",
                "error_export_failed": "Failed to export CSV",
                "error_copy_failed": "Failed to copy to clipboard",
                "error_open_failed": "Failed to open link",
                "success_copied": "Copied to clipboard!",
                "success_exported": "Successfully exported to CSV",
                "success_opened": "Opened in browser"
            }
        }
        
        # Load additional language files
        for lang_file in self.translations_dir.glob("*.json"):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                    lang_code = lang_file.stem
                    languages[lang_code] = lang_data
            except Exception as e:
                print(f"Error loading language file {lang_file}: {e}")
        
        return languages
    
    def get_available_languages(self) -> Dict[str, Dict[str, Any]]:
        """Get all available languages."""
        return self.available_languages
    
    def load_language(self, language_code: str) -> bool:
        """Load a specific language."""
        if language_code not in self.available_languages:
            print(f"Language {language_code} not available")
            return False
        
        try:
            # Load translations
            self.translations = self.available_languages[language_code]["ui"]
            self.current_language = language_code
            
            # Load Qt translator if available
            translator_file = self.translations_dir / f"{language_code}.qm"
            if translator_file.exists():
                self.app.removeTranslator(self.translator)
                self.translator = QTranslator()
                if self.translator.load(str(translator_file)):
                    self.app.installTranslator(self.translator)
            
            # Emit signal
            self.language_changed.emit(language_code)
            return True
            
        except Exception as e:
            print(f"Error loading language {language_code}: {e}")
            return False
    
    def tr(self, key: str, **kwargs) -> str:
        """Get translated text for a key with robust fallback handling."""
        try:
            # Navigate through nested keys (e.g., "table_headers.title")
            keys = key.split(".")
            value = self.translations
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    # Fallback to English if key not found
                    if self.current_language != "en":
                        en_translations = self.available_languages.get("en", {}).get("ui", {})
                        value = en_translations
                        for k in keys:
                            if isinstance(value, dict) and k in value:
                                value = value[k]
                            else:
                                return self._fallback_key(key)  # Return formatted key if not found
                    else:
                        return self._fallback_key(key)
            
            # Format with kwargs if provided
            if isinstance(value, str) and kwargs:
                try:
                    return value.format(**kwargs)
                except (KeyError, ValueError) as e:
                    print(f"Format error for key '{key}': {e}")
                    return value
            
            return str(value) if value is not None else self._fallback_key(key)
            
        except Exception as e:
            print(f"Translation error for key '{key}': {e}")
            return self._fallback_key(key)
    
    def _fallback_key(self, key: str) -> str:
        """Generate a fallback display for missing translation keys."""
        # Convert snake_case to Title Case for display
        return key.replace("_", " ").title()
    
    def tr_plural(self, key: str, count: int, **kwargs) -> str:
        """Get pluralized translated text based on count."""
        try:
            # Try to get plural form
            plural_key = f"{key}_plural" if count != 1 else key
            result = self.tr(plural_key, count=count, **kwargs)
            
            # If plural form doesn't exist, use singular and format with count
            if result == self._fallback_key(plural_key):
                singular = self.tr(key, **kwargs)
                if singular != self._fallback_key(key):
                    return singular.format(count=count, **kwargs)
            
            return result
        except Exception as e:
            print(f"Pluralization error for key '{key}': {e}")
            return self.tr(key, count=count, **kwargs)
    
    def get_current_language(self) -> str:
        """Get current language code."""
        return self.current_language
    
    def get_language_name(self, language_code: str) -> str:
        """Get display name for a language."""
        if language_code in self.available_languages:
            return self.available_languages[language_code].get("language_name", language_code)
        return language_code
    
    def detect_system_language(self) -> str:
        """Detect system language and return best matching language code."""
        try:
            # Get system locale
            system_locale = QLocale.system()
            system_lang = system_locale.name()  # e.g., "en_US", "vi_VN"
            lang_code = system_lang.split('_')[0].lower()  # Extract language part
            
            # Check if we support this language
            if lang_code in self.available_languages:
                return lang_code
            
            # Try to find a close match
            for supported_lang in self.available_languages.keys():
                if supported_lang.startswith(lang_code) or lang_code.startswith(supported_lang):
                    return supported_lang
            
            # Default to English if no match found
            return "en"
            
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"
    
    def get_language_info(self, language_code: str) -> dict:
        """Get detailed information about a language."""
        if language_code in self.available_languages:
            lang_info = self.available_languages[language_code].copy()
            lang_info['code'] = language_code
            return lang_info
        return {
            'code': language_code,
            'language_name': language_code,
            'language_native': language_code,
            'flag': '🌐'
        }
    
    def is_rtl_language(self, language_code: str) -> bool:
        """Check if a language is right-to-left."""
        rtl_languages = {'ar', 'he', 'fa', 'ur', 'yi', 'ku', 'dv'}
        return language_code in rtl_languages
    
    def get_text_direction(self, language_code: str = None) -> str:
        """Get text direction for a language."""
        if language_code is None:
            language_code = self.current_language
        return 'rtl' if self.is_rtl_language(language_code) else 'ltr'


# Global translation manager instance
_translation_manager: Optional[TranslationManager] = None


def init_translations(app: QApplication) -> TranslationManager:
    """Initialize the global translation manager."""
    global _translation_manager
    _translation_manager = TranslationManager(app)
    return _translation_manager


def get_translation_manager() -> Optional[TranslationManager]:
    """Get the global translation manager."""
    return _translation_manager


def tr(key: str, **kwargs) -> str:
    """Convenience function to get translated text."""
    if _translation_manager:
        return _translation_manager.tr(key, **kwargs)
    return key
