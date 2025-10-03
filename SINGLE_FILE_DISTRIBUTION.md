# 🚀 Single File Distribution Guide

## 🎯 **Mục tiêu: 1 file duy nhất, không cần cài đặt**

Bạn muốn tạo 1 file duy nhất mà người khác chỉ cần download và chạy, không cần clone project hay cài đặt gì thêm.

## ✅ **Đã tạo sẵn:**

### 🍎 **macOS Single File:**
- **File**: `Course_Link_Getter_Darwin_Distribution.zip` (30.6MB)
- **Nội dung**: 
  - `Course_Link_Getter` - File executable duy nhất
  - `README.txt` - Hướng dẫn sử dụng
- **Cách dùng**: Giải nén và double-click file `Course_Link_Getter`

### 🪟 **Windows Single File:**
- **File**: `Course_Link_Getter_Windows_Builder.zip` (0.2MB)
- **Nội dung**: Script để build file .exe trên Windows
- **Cách dùng**: 
  1. Gửi file này cho người có Windows
  2. Họ giải nén và chạy `BUILD_WINDOWS_EXE.bat`
  3. Họ sẽ có file `Course_Link_Getter.exe` (single file)

## 🚀 **Cách sử dụng:**

### **Option 1: macOS (Sẵn sàng ngay)**
```bash
# File đã sẵn sàng:
Course_Link_Getter_Darwin_Distribution.zip

# Cách dùng:
1. Gửi file ZIP cho người dùng macOS
2. Họ giải nén
3. Họ double-click file "Course_Link_Getter"
4. App chạy ngay lập tức!
```

### **Option 2: Windows (Cần build)**
```bash
# File build package:
Course_Link_Getter_Windows_Builder.zip

# Cách dùng:
1. Gửi file ZIP cho người có Windows
2. Họ giải nén
3. Họ chạy BUILD_WINDOWS_EXE.bat
4. Họ sẽ có Course_Link_Getter.exe
5. Họ có thể chia sẻ file .exe với ai cũng được!
```

## 📊 **Đặc điểm file single:**

### ✅ **Ưu điểm:**
- **1 file duy nhất** - Không cần cài đặt
- **Portable** - Chạy mọi nơi
- **Self-contained** - Chứa tất cả dependencies
- **26 courses** - Dữ liệu đầy đủ
- **Modern UI** - Giao diện đẹp

### 📈 **Performance:**
- **Size**: ~30-50MB
- **Startup**: 1-2 giây
- **Memory**: ~50-100MB
- **Offline**: Không cần internet

## 🎯 **Distribution Strategy:**

### **Cho macOS:**
1. **Gửi**: `Course_Link_Getter_Darwin_Distribution.zip`
2. **Người dùng**: Giải nén và chạy
3. **Kết quả**: App chạy ngay lập tức

### **Cho Windows:**
1. **Gửi**: `Course_Link_Getter_Windows_Builder.zip`
2. **Người dùng**: Build file .exe
3. **Kết quả**: Có file .exe để chia sẻ

## 🔧 **Tạo thêm file single:**

### **macOS:**
```bash
python create_single_executable.py
# Tạo: Course_Link_Getter_Darwin_Distribution.zip
```

### **Windows (trên Windows):**
```bash
python create_windows_exe.py
# Tạo: Course_Link_Getter.exe
```

## 📁 **Files đã tạo:**

```
GetLink/
├── Course_Link_Getter_Darwin_Distribution.zip    # macOS single file
├── Course_Link_Getter_Windows_Builder.zip        # Windows build package
├── dist/
│   └── Course_Link_Getter                        # macOS executable
├── create_single_executable.py                   # Script tạo single file
├── create_windows_exe.py                         # Script tạo Windows package
└── SINGLE_FILE_DISTRIBUTION.md                   # Hướng dẫn này
```

## 🎉 **Kết luận:**

### ✅ **Đã hoàn thành:**
- **macOS**: File single sẵn sàng (30.6MB)
- **Windows**: Package build sẵn sàng (0.2MB)
- **Cross-platform**: Hỗ trợ cả hai platform
- **No installation**: Không cần cài đặt gì thêm

### 🚀 **Ready to distribute:**
- **macOS users**: Gửi `Course_Link_Getter_Darwin_Distribution.zip`
- **Windows users**: Gửi `Course_Link_Getter_Windows_Builder.zip`
- **Result**: 1 file duy nhất, chạy ngay lập tức!

**Repository**: [https://github.com/HulkBetii/GetLink.git](https://github.com/HulkBetii/GetLink.git)
