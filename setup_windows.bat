@echo off
chcp 65001 >nul
echo ========================================
echo PaddleOCR Android - Windows 配置向导
echo ========================================
echo.

REM 检查 WSL 是否已安装
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] WSL 未安装
    echo.
    echo 正在安装 WSL2...
    echo 这需要管理员权限，请确认 UAC 提示
    echo.
    powershell -Command "Start-Process wsl -ArgumentList '--install' -Verb RunAs"
    echo.
    echo WSL 安装已启动。
    echo 安装完成后，请重启电脑。
    echo.
    echo 重启后，再次运行本脚本继续配置。
    pause
    exit /b
)

echo [✓] WSL 已安装
echo.

REM 检查 WSL 是否有 Ubuntu
wsl -l | findstr Ubuntu >nul
if %errorlevel% neq 0 (
    echo [!] Ubuntu 未安装
    echo 正在安装 Ubuntu...
    wsl --install -d Ubuntu
    echo.
    echo Ubuntu 安装完成！
    echo 请设置 Ubuntu 用户名和密码
    echo.
    pause
)

echo [✓] Ubuntu 已安装
echo.

REM 获取当前目录（Windows 路径）
set CURRENT_DIR=%cd%
echo 当前项目目录: %CURRENT_DIR%
echo.

REM 转换为 WSL 路径
set DRIVE=%CURRENT_DIR:~0,1%
set WSL_PATH=/mnt/%DRIVE%/%CURRENT_DIR:~3%
set WSL_PATH=%WSL_PATH:\=/%

echo WSL 路径: %WSL_PATH%
echo.

echo 接下来将在 WSL 中配置开发环境...
echo 这可能需要 10-20 分钟，请耐心等待。
echo.
pause

REM 在 WSL 中运行配置脚本
echo 复制项目到 WSL...
wsl cp -r "%WSL_PATH%" ~/PaddleOCR-Android

echo.
echo 运行配置脚本...
wsl cd ~/PaddleOCR-Android ^&^& chmod +x setup_wsl.sh ^&^& ./setup_wsl.sh

echo.
echo ========================================
echo 配置完成！
echo ========================================
echo.
echo 下一步：
echo 1. 打开 WSL 终端（从开始菜单搜索 "Ubuntu"）
echo 2. 运行：cd ~/PaddleOCR-Android
echo 3. 运行：./build.sh
echo 4. 选择选项 1（首次构建）
echo 5. 等待构建完成（30-60 分钟）
echo.
echo 或者现在就开始构建（Y/N）？
choice /c YN /n /m "请选择: "

if %errorlevel% equ 1 (
    echo.
    echo 开始构建 APK...
    wsl cd ~/PaddleOCR-Android ^&^& ./build.sh
)

echo.
echo 构建完成后，APK 文件将在 bin/ 目录下
echo 您可以在 WSL 中运行以下命令复制到 Windows 桌面：
echo   cp ~/PaddleOCR-Android/bin/*.apk /mnt/e/Desktop/
echo.
pause

