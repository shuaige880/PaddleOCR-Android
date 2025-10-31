#!/bin/bash
# 一键构建脚本

echo "========================================"
echo "PaddleOCR Android APK 构建脚本"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 buildozer 是否安装
if ! command -v buildozer &> /dev/null; then
    echo -e "${RED}错误: buildozer 未安装${NC}"
    echo "请运行: pip3 install buildozer"
    exit 1
fi

# 检查 Android SDK
if [ -z "$ANDROID_HOME" ]; then
    echo -e "${YELLOW}警告: ANDROID_HOME 未设置${NC}"
    echo "请设置 ANDROID_HOME 环境变量"
    echo "例如: export ANDROID_HOME=\$HOME/Android/Sdk"
    exit 1
fi

# 显示菜单
echo "请选择操作:"
echo "1) 首次构建（debug 版本）"
echo "2) 快速构建（debug 版本）"
echo "3) 清理缓存"
echo "4) 清理并重新构建"
echo "5) 构建发布版本"
echo "6) 部署到设备"
echo "7) 查看日志"
echo "0) 退出"
echo ""
read -p "请输入选项 [0-7]: " choice

case $choice in
    1)
        echo -e "${GREEN}开始首次构建...${NC}"
        echo "这可能需要 30-60 分钟，请耐心等待..."
        buildozer android debug
        ;;
    2)
        echo -e "${GREEN}开始快速构建...${NC}"
        buildozer android debug
        ;;
    3)
        echo -e "${YELLOW}清理缓存...${NC}"
        buildozer android clean
        echo "缓存已清理"
        ;;
    4)
        echo -e "${YELLOW}清理并重新构建...${NC}"
        buildozer android clean
        rm -rf .buildozer
        echo "开始重新构建..."
        buildozer android debug
        ;;
    5)
        echo -e "${GREEN}构建发布版本...${NC}"
        echo "注意: 需要配置签名密钥"
        buildozer android release
        ;;
    6)
        echo -e "${GREEN}部署到设备...${NC}"
        
        # 检查设备连接
        if ! command -v adb &> /dev/null; then
            echo -e "${RED}错误: adb 未找到${NC}"
            echo "请确保 Android SDK platform-tools 已安装"
            exit 1
        fi
        
        # 列出连接的设备
        echo "检查连接的设备..."
        adb devices
        
        # 查找 APK 文件
        APK_FILE=$(find bin -name "*.apk" | head -n 1)
        
        if [ -z "$APK_FILE" ]; then
            echo -e "${RED}错误: 未找到 APK 文件${NC}"
            echo "请先构建 APK"
            exit 1
        fi
        
        echo "安装 $APK_FILE ..."
        buildozer android deploy run
        ;;
    7)
        echo -e "${BLUE}查看应用日志...${NC}"
        echo "按 Ctrl+C 停止"
        buildozer android logcat | grep python
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo -e "${RED}无效选项${NC}"
        exit 1
        ;;
esac

# 构建完成提示
if [ $choice -eq 1 ] || [ $choice -eq 2 ] || [ $choice -eq 4 ] || [ $choice -eq 5 ]; then
    echo ""
    echo "========================================"
    echo -e "${GREEN}✅ 构建完成！${NC}"
    echo "========================================"
    echo ""
    echo "APK 文件位置: bin/"
    ls -lh bin/*.apk 2>/dev/null || echo "未找到 APK 文件"
    echo ""
    echo "下一步:"
    echo "- 安装到手机: adb install bin/paddleocr-*.apk"
    echo "- 或运行: buildozer android deploy run"
fi

