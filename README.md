# Course Link Getter

A desktop application for managing and searching course catalogs with advanced filtering, clipboard integration, export capabilities, and comprehensive multilingual support.

## 🎓 Features

### Core Functionality
- **Course Management**: Browse 26+ courses across 3 categories (English, Programming, Design)
- **Advanced Filtering**: Filter by category, subcategory, and text search
- **Real-time Search**: Instant filtering with debounced text search
- **Link Management**: Copy individual or bulk course links to clipboard
- **Export Capabilities**: Export filtered results to CSV
- **Popup Notifications**: Animated success notifications when copying links

### 🌍 Multilingual Support
- **10 Languages**: English, Spanish, German, Italian, Portuguese, French, Japanese, Korean, Chinese, Vietnamese
- **RTL Languages**: Full support for Arabic and Hebrew with right-to-left layouts
- **Automatic Detection**: System language detection and auto-selection
- **Real-time Switching**: Change languages without app restart
- **Localized Content**: Course titles and tags in multiple languages
- **Persistent Preferences**: Language choice saved across sessions

### User Interface
- **Desktop App**: PyQt5-based native desktop application with RTL support
- **Web Interface**: Browser-based alternative using Python HTTP server
- **Interactive CLI**: Command-line interface for quick access
- **Settings Persistence**: Automatic saving and restoration of user preferences
- **Language Selector**: Intuitive language switching with flag icons
- **RTL Layouts**: Proper right-to-left layouts for Arabic and Hebrew

### Technical Features
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Performance**: Optimized for 1000+ items with <100ms search
- **Testing**: Comprehensive pytest test suite (15 tests, <2s runtime)
- **CI/CD**: GitHub Actions workflows for continuous integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HulkBetii/GetLink.git
   cd GetLink/course_link_getter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Desktop app (PyQt5) - Recommended
   python launch_pyqt5.py
   
   # Alternative launchers
   python app_pyqt5.py
   python app.py
   
   # Web interface
   python web_app.py
   
   # Interactive CLI
   python simple_ui.py
   ```

## 📱 User Interfaces

### 1. Desktop Application (PyQt5)
- Native desktop experience with multilingual support
- Advanced filtering panel with RTL layouts
- Sortable table view with localized headers
- Context menus and keyboard shortcuts
- Settings persistence and language preferences
- Language selector with flag icons
- RTL support for Arabic and Hebrew

### 2. Web Interface
- Browser-based interface
- Access at `http://localhost:8081`
- Mobile-friendly responsive design
- Real-time filtering

### 3. Command Line Interface
- Interactive menu system
- Quick course browsing
- Clipboard integration
- CSV export functionality

## 🔧 Development

### Project Structure
```
course_link_getter/
├── core/                    # Core business logic
│   ├── models.py           # Pydantic data models with multilingual support
│   ├── store.py            # CatalogStore for data management
│   ├── settings.py         # Settings persistence
│   ├── translations.py     # Translation system with RTL support
│   └── translations/       # Language translation files
│       ├── en.json         # English (default)
│       ├── ar.json         # Arabic (RTL)
│       ├── he.json         # Hebrew (RTL)
│       ├── es.json         # Spanish
│       ├── de.json         # German
│       ├── it.json         # Italian
│       ├── pt.json         # Portuguese
│       ├── fr.json         # French
│       ├── ja.json         # Japanese
│       ├── ko.json         # Korean
│       ├── zh.json         # Chinese
│       └── vi.json         # Vietnamese
├── ui_pyqt5/               # PyQt5 desktop UI
│   ├── main_window.py      # Main application window with RTL support
│   └── widgets/           # UI components
│       ├── language_selector.py  # Language selection widget
│       ├── rtl_helper.py   # RTL support utilities
│       └── results_view.py # Multilingual table view
├── tests/                  # Test suite
│   └── test_store.py       # Comprehensive pytest tests
├── assets/                 # Sample data
│   ├── catalog.sample.json # Legacy course catalog
│   └── catalog.multilingual.json # Multilingual course catalog
└── requirements.txt        # Dependencies
```

### Running Tests
```bash
# Quick tests (CI-friendly)
make test-quick

# Verbose tests
make test

# With coverage
python -m pytest tests/test_store.py --cov=core --cov-report=term-missing
```

### CI/CD
The project includes GitHub Actions workflows:
- **`.github/workflows/ci.yml`** - Simple CI workflow
- **`.github/workflows/test.yml`** - Comprehensive testing with coverage

## 📊 Course Data

### Categories
- **English**: IELTS, TOEIC, Speaking
- **Programming**: Python, Web, Data
- **Design**: UI/UX, Graphic

### Sample Data
- 26 courses with diverse providers
- Valid HTTP links for all courses
- Comprehensive tags and metadata
- Real-world course examples

### 🌍 Multilingual Data
- **Multilingual Catalog**: Course titles and tags in 10 languages
- **RTL Support**: Arabic and Hebrew course content
- **Backward Compatibility**: Legacy single-language catalogs supported
- **Dynamic Loading**: Language-specific data loading
- **Fallback System**: English fallback for missing translations

## 🌍 Multilingual Features

### Supported Languages
- **🇺🇸 English** (Default)
- **🇪🇸 Spanish** (Español)
- **🇩🇪 German** (Deutsch)
- **🇮🇹 Italian** (Italiano)
- **🇵🇹 Portuguese** (Português)
- **🇫🇷 French** (Français)
- **🇯🇵 Japanese** (日本語)
- **🇰🇷 Korean** (한국어)
- **🇨🇳 Chinese** (中文)
- **🇻🇳 Vietnamese** (Tiếng Việt)
- **🇸🇦 Arabic** (العربية) - RTL
- **🇮🇱 Hebrew** (עברית) - RTL

### Language Features
- **Automatic Detection**: Detects system language on first run
- **Real-time Switching**: Change languages without restarting
- **RTL Support**: Full right-to-left layout for Arabic and Hebrew
- **Localized Content**: Course titles and tags in native languages
- **Persistent Preferences**: Language choice saved across sessions
- **Fallback System**: English fallback for missing translations

### RTL Language Support
- **Automatic Layout**: RTL layouts applied automatically
- **Text Direction**: Proper right-to-left text alignment
- **UI Positioning**: RTL-aware notification and widget positioning
- **Reading Flow**: Natural reading experience for RTL languages

## 🛠️ Configuration

### Settings Persistence
- User preferences saved automatically
- Cross-platform data directory using `platformdirs`
- Filter states restored on startup
- Window size and position remembered
- Language preferences persisted across sessions
- RTL layout preferences maintained

### Export Options
- **CSV Export**: title, category, subcategory, provider, link
- **Clipboard**: Individual or bulk link copying
- **Formats**: Newline-separated links for easy pasting

## 🧪 Testing

### Test Coverage
- **15 comprehensive test cases**
- **Runtime**: <2 seconds (CI-friendly)
- **Coverage**: 83% for core functionality
- **Performance**: Validated for 1000+ items

### Test Categories
- Data loading and validation
- Filter functionality (all combinations)
- Model validation
- Performance benchmarks
- Error handling

## 📈 Performance

### Benchmarks
- **Search Performance**: <100ms for 1000+ items
- **Filter Operations**: <1ms for category filtering
- **Memory Usage**: Optimized for large datasets
- **Startup Time**: <2 seconds with data loading

### Optimization
- Efficient filtering algorithms
- Debounced search (100ms delay)
- Lazy loading for large datasets
- Memory-efficient data structures

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation
- Ensure CI tests pass

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Repository**: [https://github.com/HulkBetii/GetLink.git](https://github.com/HulkBetii/GetLink.git)
- **Issues**: [GitHub Issues](https://github.com/HulkBetii/GetLink/issues)
- **Actions**: [GitHub Actions](https://github.com/HulkBetii/GetLink/actions)

## 🎯 Roadmap

### Planned Features
- [ ] Database backend support
- [ ] Advanced search operators
- [ ] Course rating and reviews
- [ ] Bulk import/export
- [ ] Plugin system
- [ ] Mobile app version

### Recent Updates
- ✅ **Multilingual Support**: 10 languages with complete UI translations
- ✅ **RTL Language Support**: Arabic and Hebrew with right-to-left layouts
- ✅ **Translation System**: Robust fallback handling and pluralization
- ✅ **Language Detection**: Automatic system language detection
- ✅ **Multilingual Data**: Course titles and tags in multiple languages
- ✅ Settings persistence implementation
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline setup
- ✅ Performance optimizations
- ✅ Cross-platform compatibility

---

**Course Link Getter** - Your comprehensive solution for course catalog management! 🎓✨