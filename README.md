# 🎯 PaddleOCR Android 版本

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2.1-green.svg)](https://kivy.org/)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-2.7+-orange.svg)](https://github.com/PaddlePaddle/PaddleOCR)
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](LICENSE)

将 PaddleOCR 桌面应用转换为 Android 移动应用，支持拍照识别、相册选择，中文识别准确率 97%+。

## ✨ 功能特性

- 📷 **相机拍照**: 直接拍照进行文字识别
- 🖼️ **相册选择**: 从手机相册选择图片
- 🎯 **高精度识别**: PaddleOCR 引擎，中文识别准确率 97%+
- 📋 **一键复制**: 识别结果一键复制到剪贴板
- 📊 **置信度显示**: 每行文字显示识别置信度
- 🔒 **隐私保护**: 所有识别在本地完成，不上传服务器
- 📱 **广泛兼容**: 支持 Android 5.0+ 系统
- 💾 **离线使用**: 首次下载模型后可完全离线使用

## 📸 应用截图

```
┌─────────────────────────────┐
│  🎯 PaddleOCR 移动版        │
├─────────────────────────────┤
│ [📷拍照] [🖼️相册]          │
│ [🚀识别] [📋复制]          │
├─────────────────────────────┤
│                             │
│     [图片预览区域]          │
│                             │
├─────────────────────────────┤
│  识别结果:                  │
│  1. 文字内容 (98.5%)        │
│  2. 更多文字 (97.2%)        │
│  ...                        │
└─────────────────────────────┘
```

## 🚀 快速开始

### 📥 下载安装

#### 方式一：下载 APK（推荐）
1. 前往 [Releases](../../releases) 页面
2. 下载最新的 `paddleocr-x.x.x.apk`
3. 在手机上安装

#### 方式二：自己构建
详见下方构建说明

### 🎮 使用方法

1. 打开应用
2. 点击 **📷拍照** 拍摄照片，或点击 **🖼️相册** 选择图片
3. 点击 **🚀识别** 开始 OCR 识别
4. 查看识别结果，点击 **📋复制** 复制文字

> **首次使用**: 需要联网下载 OCR 模型（约 20MB），请连接 WiFi

## 🛠️ 自己构建 APK

### Windows 用户（3 种方式）

#### ⭐ 方式一：使用 GitHub Actions（最简单）
**无需安装任何环境，完全在云端构建**

1. 将代码上传到 GitHub
2. GitHub Actions 自动构建
3. 下载构建好的 APK

📖 详细教程：[使用说明-GitHub构建.md](使用说明-GitHub构建.md)

#### ⭐ 方式二：使用 WSL2（推荐）
**在 Windows 中使用 Linux 环境**

```bash
# 1. 安装 WSL2（PowerShell 管理员模式）
wsl --install

# 2. 重启电脑后，运行配置脚本
.\setup_windows.bat

# 3. 在 WSL 中构建
wsl
cd ~/PaddleOCR-Android
./build.sh
```

📖 详细教程：[快速开始.md](快速开始.md)

#### 方式三：使用虚拟机
安装 Ubuntu 虚拟机，按 Linux 步骤操作

### Linux 用户

```bash
# 1. 运行自动配置脚本
chmod +x setup_wsl.sh
./setup_wsl.sh

# 2. 构建 APK
chmod +x build.sh
./build.sh

# 3. 获取 APK
# bin/paddleocr-1.0.0-arm64-v8a-debug.apk
```

### macOS 用户

```bash
# 1. 安装依赖
brew install python3 git openjdk@11
pip3 install buildozer

# 2. 配置 Android SDK（下载 Android Studio）

# 3. 构建
./build.sh
```

## 📚 文档导航

| 文档 | 说明 | 适合人群 |
|-----|------|---------|
| [简易说明.txt](简易说明.txt) | 最简单的说明，纯文本 | 所有用户 ⭐⭐⭐⭐⭐ |
| [快速开始.md](快速开始.md) | 快速入门指南 | 新手用户 ⭐⭐⭐⭐ |
| [使用说明-GitHub构建.md](使用说明-GitHub构建.md) | GitHub Actions 云构建教程 | Windows 用户 ⭐⭐⭐⭐⭐ |
| [README_Android.md](README_Android.md) | 详细技术文档 | 开发者 ⭐⭐⭐ |
| [项目说明.md](项目说明.md) | 项目架构和技术细节 | 开发者 ⭐⭐⭐ |

## 🎬 构建步骤（简化版）

```bash
# Linux/WSL 用户
./setup_wsl.sh    # 自动配置环境（首次）
./build.sh        # 构建 APK

# 或手动构建
buildozer android debug
```

**构建时间**：首次 30-60 分钟，后续 5-10 分钟

**APK 位置**：`bin/paddleocr-1.0.0-arm64-v8a-debug.apk`

## 📦 项目结构

```
PaddleOCR-Android/
├── main.py                      # Android 应用主程序 ⭐
├── paddle_ocr.py                # 原桌面版程序（保留）
├── buildozer.spec               # APK 构建配置 ⭐
├── requirements.txt             # Python 依赖
│
├── setup_wsl.sh                 # WSL 自动配置脚本
├── build.sh                     # 一键构建脚本
├── setup_windows.bat            # Windows 配置向导
├── test_kivy.py                 # Kivy 测试程序
│
├── README.md                    # 本文件
├── 简易说明.txt                 # 最简单的说明
├── 快速开始.md                  # 快速入门
├── README_Android.md            # 详细文档
├── 项目说明.md                  # 项目架构
└── 使用说明-GitHub构建.md       # GitHub 构建教程
```

## 🔧 技术栈

- **GUI 框架**: Kivy 2.2.1（跨平台）
- **OCR 引擎**: PaddleOCR 2.7.0.3（高精度）
- **深度学习**: PaddlePaddle Tiny（轻量级）
- **构建工具**: Buildozer（Python to APK）
- **图像处理**: Pillow, OpenCV
- **支持系统**: Android 5.0+ (API 21+)
- **支持架构**: ARM64, ARMv7

## 📊 性能指标

| 指标 | 数值 |
|-----|------|
| 中文识别准确率 | 97%+ |
| APK 大小 | 40-60 MB |
| 首次启动时间 | 3-5 秒 |
| OCR 识别速度 | 1-3 秒/张 |
| 最低 Android 版本 | 5.0 |
| 模型下载大小 | ~20 MB |

## ❓ 常见问题

<details>
<summary><b>Q: Windows 如何构建？</b></summary>

必须使用 WSL2 或 Linux 虚拟机。Buildozer 不支持原生 Windows。

推荐使用 GitHub Actions 云构建，无需配置环境。
</details>

<details>
<summary><b>Q: 构建时间太长？</b></summary>

首次构建需要下载大量依赖（1-2GB），约 30-60 分钟。

后续构建会使用缓存，只需 5-10 分钟。
</details>

<details>
<summary><b>Q: 识别速度慢？</b></summary>

- 已使用轻量级模型（paddlepaddle-tiny）
- 避免识别过大图片（自动压缩）
- 关闭后台应用释放资源
</details>

<details>
<summary><b>Q: 模型下载失败？</b></summary>

首次运行需要联网下载模型：
- 连接稳定的 WiFi
- 等待 1-2 分钟
- 下载后永久缓存
</details>

<details>
<summary><b>Q: 应用闪退？</b></summary>

查看日志：
```bash
adb logcat | grep python
```

常见原因：
- 权限未授予（相机、存储）
- 内存不足
- 模型未下载完成
</details>

## 🔒 隐私与安全

- ✅ **本地处理**: 所有 OCR 识别在设备本地完成
- ✅ **不上传数据**: 不会上传图片或识别结果到服务器
- ✅ **不收集信息**: 不收集任何用户信息
- ✅ **临时文件**: 照片仅临时保存，关闭应用自动清理
- ✅ **权限最小化**: 仅请求必需的权限

### 所需权限

| 权限 | 用途 |
|-----|------|
| 相机 | 拍照功能 |
| 读取存储 | 从相册选择图片 |
| 写入存储 | 保存临时照片 |
| 网络 | 首次下载 OCR 模型 |

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目依赖的开源项目：
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Apache License 2.0
- [Kivy](https://github.com/kivy/kivy) - MIT License
- [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) - Apache License 2.0

## 🙏 致谢

感谢以下开源项目：
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 提供高精度 OCR 引擎
- [Kivy](https://kivy.org/) - 跨平台 Python GUI 框架
- [Buildozer](https://github.com/kivy/buildozer) - Python to Android 打包工具

## 📞 支持

- 📖 查看文档：[快速开始.md](快速开始.md)
- 🐛 报告问题：[GitHub Issues](../../issues)
- 💡 功能建议：[GitHub Discussions](../../discussions)

## 🌟 Star History

如果这个项目对您有帮助，请给个 Star ⭐

---

**开发状态**: ✅ 稳定可用

**最后更新**: 2025-10-31

Made with ❤️ using Python, Kivy, and PaddleOCR

