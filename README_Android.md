# PaddleOCR Android 应用

将 PaddleOCR 桌面应用转换为 Android 移动应用。

## 📱 功能特性

- ✅ **拍照识别**：直接使用手机相机拍照进行 OCR 识别
- ✅ **相册选择**：从手机相册选择图片进行识别
- ✅ **高精度识别**：使用 PaddleOCR 引擎，中文识别准确率 97%+
- ✅ **结果复制**：一键复制识别结果到剪贴板
- ✅ **置信度显示**：每行文字都显示识别置信度
- ✅ **离线使用**：模型下载后可离线使用

## 🛠️ 构建步骤

### 1. 安装依赖

#### Ubuntu/Debian Linux:
```bash
# 安装系统依赖
sudo apt update
sudo apt install -y python3-pip python3-dev build-essential \
    git zip unzip openjdk-11-jdk autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev

# 安装 Android SDK 和 NDK
# 下载 Android Studio 或者 Command Line Tools
# 设置环境变量：
export ANDROID_HOME=$HOME/Android/Sdk
export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/23.1.7779620
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

#### Windows:
```powershell
# 安装 Python 3.8+
# 下载并安装 Android Studio
# 安装 Java JDK 11+

# 设置环境变量（PowerShell）:
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"
$env:ANDROID_NDK_HOME = "$env:ANDROID_HOME\ndk\23.1.7779620"
```

### 2. 安装 Buildozer

```bash
# Linux
pip3 install --upgrade buildozer cython

# Windows (需要 WSL 或 Linux 虚拟机)
# Buildozer 目前仅支持 Linux/macOS
```

**注意**：Windows 用户需要使用 WSL2 或 Linux 虚拟机来运行 Buildozer。

### 3. 构建 APK

```bash
# 初次构建（会自动下载依赖，需要较长时间）
buildozer android debug

# 构建完成后，APK 文件在 bin/ 目录
# 例如: bin/paddleocr-1.0.0-arm64-v8a-debug.apk
```

### 4. 安装到手机

```bash
# 通过 USB 连接手机，启用 USB 调试
adb install bin/paddleocr-1.0.0-arm64-v8a-debug.apk

# 或者直接部署并运行
buildozer android deploy run
```

## 📦 发布版本

构建发布版本（需要签名）:

```bash
# 生成签名密钥
keytool -genkey -v -keystore paddleocr.keystore -alias paddleocr \
    -keyalg RSA -keysize 2048 -validity 10000

# 构建发布版
buildozer android release

# 手动签名（如果需要）
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
    -keystore paddleocr.keystore \
    bin/paddleocr-1.0.0-arm64-v8a-release-unsigned.apk paddleocr

# 对齐 APK
zipalign -v 4 bin/paddleocr-1.0.0-arm64-v8a-release-unsigned.apk \
    bin/paddleocr-1.0.0-release.apk
```

## 🎯 使用说明

1. **启动应用**：在手机上打开 PaddleOCR 应用
2. **拍照或选择图片**：
   - 点击 "📷 拍照" 按钮直接拍照
   - 点击 "🖼️ 相册" 按钮从相册选择图片
3. **开始识别**：点击 "🚀 识别" 按钮开始 OCR 识别
4. **查看结果**：识别完成后在结果区域显示
5. **复制结果**：点击 "📋 复制" 按钮复制识别文字

## ⚙️ 配置说明

### buildozer.spec 主要配置

- `android.permissions`：应用所需权限
  - CAMERA：相机权限
  - READ_EXTERNAL_STORAGE：读取存储权限
  - WRITE_EXTERNAL_STORAGE：写入存储权限
  - INTERNET：网络权限（首次下载模型需要）

- `android.api`：目标 Android API 级别（31 = Android 12）
- `android.minapi`：最低 Android API 级别（21 = Android 5.0）
- `android.archs`：支持的 CPU 架构
  - arm64-v8a：64位 ARM（现代手机）
  - armeabi-v7a：32位 ARM（老设备）

### 优化建议

1. **减小 APK 体积**：
   ```spec
   # 只构建 arm64-v8a 架构
   android.archs = arm64-v8a
   ```

2. **加快构建速度**：
   ```bash
   # 使用缓存
   buildozer android debug
   
   # 清理后重新构建
   buildozer android clean
   buildozer android debug
   ```

3. **调试日志**：
   ```bash
   # 实时查看应用日志
   buildozer android deploy run logcat
   
   # 或使用 adb
   adb logcat | grep python
   ```

## 🐛 常见问题

### 1. 构建失败

```bash
# 清理缓存重试
buildozer android clean
rm -rf .buildozer/
buildozer android debug
```

### 2. 权限问题

- 确保在手机设置中授予应用相机和存储权限
- Android 6.0+ 需要运行时权限，应用会自动请求

### 3. PaddleOCR 模型下载慢

- 首次运行需要下载模型（约 20MB）
- 确保手机连接 WiFi
- 模型下载后会缓存，可离线使用

### 4. 识别速度慢

- 使用 paddlepaddle-tiny 轻量版（已配置）
- 避免识别过大的图片（自动缩放）
- 关闭不必要的后台应用

### 5. Windows 构建问题

- Buildozer 不支持 Windows，请使用 WSL2
- 安装 WSL2: `wsl --install`
- 在 WSL2 中按 Linux 步骤操作

## 📊 性能优化

1. **模型加载**：首次加载较慢，后续使用单例模式复用
2. **图片处理**：自动压缩大图片，提高识别速度
3. **内存管理**：识别后自动释放临时资源

## 🔒 安全说明

- 所有 OCR 识别在本地完成，不上传服务器
- 照片仅临时保存，应用关闭后自动清理
- 需要的权限：
  - 相机：拍照功能
  - 存储：读取/保存图片
  - 网络：仅用于首次下载模型

## 📄 许可证

与原 PaddleOCR 项目保持一致

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请参考：
- [Kivy 文档](https://kivy.org/doc/stable/)
- [Buildozer 文档](https://buildozer.readthedocs.io/)
- [PaddleOCR 文档](https://github.com/PaddlePaddle/PaddleOCR)

---

**提示**：首次构建需要下载大量依赖（约 1-2GB），请耐心等待并确保网络稳定。

