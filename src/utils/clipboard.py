import subprocess
import sys
from typing import List
from ..models import Course


class ClipboardManager:
    """Handles clipboard operations for course links."""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
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
    
    @staticmethod
    def copy_course_link(course: Course) -> bool:
        """Copy a single course link to clipboard."""
        return ClipboardManager.copy_to_clipboard(course.link)
    
    @staticmethod
    def copy_all_links(courses: List[Course]) -> bool:
        """Copy all course links to clipboard, one per line."""
        links = [course.link for course in courses]
        links_text = "\n".join(links)
        return ClipboardManager.copy_to_clipboard(links_text)
    
    @staticmethod
    def open_in_browser(url: str) -> bool:
        """Open URL in default browser."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", url], check=True)
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", url], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", url], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
