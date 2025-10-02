# 🚀 Course Link Getter - Run Instructions

This guide shows how to run the Course Link Getter desktop application in Cursor's integrated terminal.

## 📋 Prerequisites

- Python 3.11+ installed
- Cursor IDE with integrated terminal
- Git (for cloning the repository)

## 🛠️ Setup Instructions

### 1️⃣ Create & Activate Virtual Environment

#### Windows PowerShell:
```powershell
# Navigate to project directory
cd GetLink

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

#### macOS/Linux:
```bash
# Navigate to project directory
cd GetLink

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 2️⃣ Install Dependencies

#### Using requirements.txt (Recommended):
```bash
# Install all dependencies
pip install -r requirements.txt
```

#### Using Poetry (Alternative):
```bash
# Install Poetry if not already installed
pip install poetry

# Install dependencies
poetry install
```

### 3️⃣ Run the Application

The project provides multiple entry points for different environments:

#### Option A: PyQt6 Version (Primary)
```bash
# Navigate to course_link_getter directory
cd course_link_getter

# Run PyQt6 version (recommended launcher)
python launch_pyqt6.py

# Or run directly
python app.py
```

#### Option B: PyQt5 Version (Fallback)
```bash
# Navigate to course_link_getter directory
cd course_link_getter

# Run PyQt5 version (recommended launcher)
python launch_pyqt5.py

# Or run directly
python app_pyqt5.py
```

#### Option C: Web Interface (Browser-based)
```bash
# Navigate to course_link_getter directory
cd course_link_getter

# Run web interface
python web_app.py

# Then open browser to: http://localhost:8080
# (or the port shown in terminal output)
```

#### Option D: Command Line Interface
```bash
# Navigate to course_link_getter directory
cd course_link_getter

# Run CLI version
python demo_cli.py
```

## 🔧 Troubleshooting

### PyQt6 Issues

If you encounter PyQt6 errors like `"qt.qpa.plugin"` or import issues:

```bash
# Install additional PyQt6 components
pip install PyQt6-Qt6 PyQt6-sip

# Or reinstall PyQt6
pip uninstall PyQt6
pip install PyQt6==6.6.1
```

### Font/UTF-8 Issues

#### Windows PowerShell:
```powershell
# Set UTF-8 environment variable
$env:PYTHONUTF8=1

# Then run the app
python app.py
```

#### macOS/Linux:
```bash
# Set UTF-8 environment variable
export PYTHONUTF8=1

# Then run the app
python app.py
```

### Port Already in Use (Web App)

If port 8080 is already in use:

```bash
# Find process using port 8080
lsof -i :8080

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or the web app will automatically try other ports (8081, 8082, etc.)
```

## 📁 Project Structure

```
GetLink/
├── course_link_getter/          # Main application directory
│   ├── app.py                   # PyQt6 entry point
│   ├── app_pyqt5.py            # PyQt5 entry point
│   ├── web_app.py              # Web interface
│   ├── demo_cli.py             # CLI interface
│   ├── requirements.txt        # Dependencies
│   ├── core/                   # Business logic
│   ├── ui/                     # PyQt6 UI components
│   ├── ui_pyqt5/              # PyQt5 UI components
│   ├── assets/                # Sample data
│   └── tests/                 # Test suite
├── README.md                   # Project documentation
├── RUN.md                     # This file
└── requirements.txt           # Root dependencies
```

## 🎯 Quick Start Commands

### One-liner setup (macOS/Linux):
```bash
cd GetLink && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cd course_link_getter && python launch_pyqt5.py
```

### One-liner setup (Windows PowerShell):
```powershell
cd GetLink; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; cd course_link_getter; python launch_pyqt5.py
```

### Web Interface (Always Works):
```bash
cd GetLink/course_link_getter && python web_app.py
# Then open: http://localhost:8080
```

## ✅ Verification

After running the app, you should see:

1. **Desktop App**: A window titled "Course Link Getter" with:
   - Category/Subcategory dropdowns
   - Search box
   - Results table with course data
   - Toolbar with export/copy options

2. **Web App**: Browser interface at `http://localhost:8080` (or similar port)

3. **CLI App**: Interactive command-line interface with course browsing

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed project information
- Review [TESTING_SUMMARY.md](course_link_getter/TESTING_SUMMARY.md) for test information
- Ensure all dependencies are installed correctly
- Try the PyQt5 version if PyQt6 has compatibility issues
- Use the web interface as a fallback option

## 🎉 Success!

If you see the Course Link Getter interface, you're ready to:
- Browse 26+ courses across 3 categories
- Filter by category, subcategory, and text search
- Copy links to clipboard
- Export results to CSV
- Use keyboard shortcuts and context menus

Happy course browsing! 🎓✨
