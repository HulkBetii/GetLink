# Windows Build Guide

Hướng dẫn build Course Link Getter cho Windows với 2 output: installer .exe và portable .exe.

## 🚀 Quick Start

### Lệnh duy nhất để build:
```bash
python build_windows.py
```

## 📋 Yêu cầu hệ thống

### Tự động cài đặt:
- ✅ **Python 3.8+** - Script sẽ kiểm tra và hướng dẫn
- ✅ **PyInstaller** - Tự động cài đặt nếu thiếu
- ✅ **NSIS** - Tự động tải portable version nếu thiếu
- ✅ **UPX** - Tự động tải để nén executable

### Hệ điều hành:
- **Windows 10/11 x64** (khuyến nghị)
- **macOS/Linux** (cross-compile, cần test trên Windows)

## 📦 Output Files

Sau khi build thành công, bạn sẽ có:

### 1. Portable Executable
- **File**: `release/Course_Link_Getter-Portable.exe`
- **Kích thước**: ~35-50 MB
- **Cách dùng**: Chạy trực tiếp, không cần cài đặt
- **Tính năng**: 
  - Tự chứa Python runtime
  - Tự chứa tất cả dependencies
  - Không cần cài đặt thêm gì

### 2. Installer Package
- **File**: `release/Course_Link_Getter-Setup-x64.exe`
- **Kích thước**: ~40-60 MB
- **Cách dùng**: Double-click để cài đặt
- **Tính năng**:
  - Cài vào `%ProgramFiles%\Course Link Getter\`
  - Tạo shortcut Desktop và Start Menu
  - Có Uninstall trong Control Panel
  - Đăng ký trong Windows Registry

### 3. Verification Files
- **File**: `release/checksums.txt` - SHA256 checksums
- **File**: `smoketest.ps1` - Script kiểm thử tự động

## 🔧 Build Process

### Tự động thực hiện:
1. **Pre-flight checks** - Kiểm tra Python, tools
2. **Download tools** - Tải NSIS, UPX nếu thiếu
3. **Create venv** - Tạo môi trường build riêng
4. **Install deps** - Cài PyQt5, pydantic, PyInstaller
5. **Build portable** - PyInstaller --onefile
6. **Compress** - UPX compression (nếu có)
7. **Create installer** - NSIS script generation
8. **Build installer** - Compile NSIS installer
9. **Create checksums** - SHA256 verification
10. **Cleanup** - Xóa temp files

### Manual steps (nếu cần):
```bash
# Cài đặt NSIS thủ công (nếu auto-download fail)
# Download từ: https://nsis.sourceforge.io/Download

# Cài đặt UPX thủ công (nếu auto-download fail)  
# Download từ: https://upx.github.io/
```

## 🧪 Testing

### Automated Test:
```powershell
# Chạy smoketest tự động
powershell -ExecutionPolicy Bypass -File smoketest.ps1
```

### Manual Test:
1. **Portable**: Double-click `Course_Link_Getter-Portable.exe`
2. **Installer**: Run `Course_Link_Getter-Setup-x64.exe`
3. **Verify**: App mở được, hiển thị 26 courses, copy link hoạt động

## 📁 Project Structure

```
GetLink/
├── build_windows.py          # Main build script
├── smoketest.ps1             # Automated test script
├── installer.nsi             # NSIS installer script (auto-generated)
├── LICENSE.txt               # License file (auto-generated)
├── course_link_getter/       # Source code
│   ├── assets/icon.ico       # App icon
│   ├── requirements.txt      # Dependencies
│   └── launch_pyqt5.py      # Entry point
├── build/                    # PyInstaller temp files
├── dist/                     # PyInstaller output
├── release/                  # Final distribution files
│   ├── Course_Link_Getter-Portable.exe
│   ├── Course_Link_Getter-Setup-x64.exe
│   └── checksums.txt
└── tools/                    # Downloaded tools (NSIS, UPX)
```

## 🐛 Troubleshooting

### Lỗi thường gặp:

#### 1. "PyInstaller not found"
```bash
# Script sẽ tự cài, hoặc cài thủ công:
pip install pyinstaller
```

#### 2. "NSIS not found"
```bash
# Script sẽ tự tải, hoặc cài thủ công:
# Download từ: https://nsis.sourceforge.io/
```

#### 3. "Permission denied"
```bash
# Chạy với quyền admin trên Windows
# Hoặc chạy từ terminal với quyền admin
```

#### 4. "App không mở được"
```bash
# Kiểm tra Windows Defender
# Thêm exception cho thư mục release/
# Hoặc chạy: Set-MpPreference -ExclusionPath "C:\path\to\release"
```

#### 5. "Missing DLL"
```bash
# Script đã nhúng tất cả dependencies
# Nếu vẫn lỗi, cài Visual C++ Redistributable:
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

## 📊 Build Statistics

### Typical build times:
- **First build**: 2-5 minutes (download tools)
- **Subsequent builds**: 30-60 seconds
- **Clean build**: 1-2 minutes

### File sizes:
- **Portable**: 35-50 MB (depends on compression)
- **Installer**: 40-60 MB (includes NSIS overhead)
- **Source**: ~2 MB (uncompressed)

## 🎯 Distribution

### Cho end users:
1. **Portable**: Gửi file `.exe`, họ chạy trực tiếp
2. **Installer**: Gửi file `.exe`, họ cài đặt như app thông thường

### Cho developers:
1. **Source**: Clone repo, chạy `python build_windows.py`
2. **CI/CD**: Integrate script vào build pipeline

## 📝 Notes

- **Cross-platform**: Script chạy được trên macOS/Linux để build Windows
- **Self-contained**: Không cần cài Python trên máy target
- **Auto-dependency**: Tự động xử lý tất cả dependencies
- **Production-ready**: Đã test trên Windows 10/11 x64

## 🆘 Support

Nếu gặp vấn đề:
1. Chạy `python build_windows.py` với verbose output
2. Kiểm tra log trong console
3. Chạy `smoketest.ps1` để verify
4. Check Windows Defender/antivirus settings
