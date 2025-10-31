#!/bin/bash
# WSL2 环境自动配置脚本
# 用于 Windows 用户在 WSL2 中构建 Android APK

echo "========================================"
echo "PaddleOCR Android 开发环境配置"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在 WSL 中
if ! grep -qi microsoft /proc/version; then
    echo -e "${YELLOW}警告: 似乎不在 WSL 环境中${NC}"
fi

# 更新系统
echo -e "${GREEN}[1/7] 更新系统包...${NC}"
sudo apt update
sudo apt upgrade -y

# 安装基础工具
echo -e "${GREEN}[2/7] 安装基础工具...${NC}"
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    zip \
    unzip \
    curl \
    wget \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    openjdk-11-jdk

# 安装 Python 工具
echo -e "${GREEN}[3/7] 安装 Python 工具...${NC}"
pip3 install --upgrade pip
pip3 install --upgrade buildozer cython

# 创建 Android SDK 目录
echo -e "${GREEN}[4/7] 配置 Android SDK...${NC}"
ANDROID_HOME="$HOME/Android/Sdk"
mkdir -p "$ANDROID_HOME"

# 下载 Android Command Line Tools（如果还没有）
if [ ! -d "$ANDROID_HOME/cmdline-tools/latest" ]; then
    echo "下载 Android Command Line Tools..."
    cd ~
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
    unzip -q commandlinetools-linux-9477386_latest.zip
    mkdir -p "$ANDROID_HOME/cmdline-tools"
    mv cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"
    rm commandlinetools-linux-9477386_latest.zip
    echo "Android Command Line Tools 已安装"
else
    echo "Android Command Line Tools 已存在"
fi

# 设置环境变量
echo -e "${GREEN}[5/7] 设置环境变量...${NC}"
if ! grep -q "ANDROID_HOME" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# Android SDK
export ANDROID_HOME=$HOME/Android/Sdk
export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/23.1.7779620
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator
EOF
    echo "环境变量已添加到 ~/.bashrc"
fi

# 加载环境变量
source ~/.bashrc

# 安装 Android SDK 组件
echo -e "${GREEN}[6/7] 安装 Android SDK 组件...${NC}"
echo "这可能需要几分钟，请耐心等待..."

yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-31" \
    "build-tools;31.0.0" \
    "ndk;23.1.7779620" \
    "cmake;3.18.1"

# 验证安装
echo -e "${GREEN}[7/7] 验证安装...${NC}"
echo ""
echo "Python 版本:"
python3 --version

echo ""
echo "Pip 版本:"
pip3 --version

echo ""
echo "Java 版本:"
java -version

echo ""
echo "Buildozer 版本:"
buildozer --version

echo ""
echo "Android SDK 位置:"
echo "$ANDROID_HOME"

echo ""
echo "已安装的 Android 组件:"
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list_installed

echo ""
echo "========================================"
echo -e "${GREEN}✅ 安装完成！${NC}"
echo "========================================"
echo ""
echo "下一步："
echo "1. 重新加载环境变量: source ~/.bashrc"
echo "2. 进入项目目录: cd /mnt/e/Desktop/ORC"
echo "3. 构建 APK: buildozer android debug"
echo ""
echo "注意："
echo "- 首次构建需要 30-60 分钟"
echo "- 需要良好的网络连接"
echo "- 确保有足够的磁盘空间（至少 10GB）"
echo ""
echo "遇到问题？查看 快速开始.md 文件"
echo ""

