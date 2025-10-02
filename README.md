# Course Link Getter

Lightweight PyQt5 desktop app to search a course catalog.

## Features
- Category, Subcategory, and Text filtering with instant updates
- Copy single/bulk links with animated success notification
- Proportional table layout (Title 1/2; Category 2/5; Subcategory 2/5; Actions 1/5)
- Minimal transparent scrollbars; modern light theme

## Quick start
```bash
git clone https://github.com/HulkBetii/GetLink.git
cd GetLink/course_link_getter
pip install -r requirements.txt
python launch_pyqt5.py
```

## Run tests
```bash
cd GetLink/course_link_getter
pytest -q tests/test_store.py
```

## Project layout
```
course_link_getter/
├── assets/
│   ├── catalog.sample.json
│   └── catalog.multilingual.json
├── core/
│   ├── models.py
│   ├── settings.py
│   ├── store.py
│   └── translations.py  
├── ui_pyqt5/
│   ├── main_window.py
│   └── widgets/
│       ├── language_selector.py  
│       ├── results_view.py
│       ├── rtl_helper.py  
│       └── toolbar.py
├── launch_pyqt5.py
├── requirements.txt
└── tests/
    └── test_store.py
```

## Notes
- Recommended Python 3.11+
- Multilingual/RTL features disabled; app uses single-language legacy catalog only

MIT License