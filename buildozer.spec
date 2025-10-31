[app]

# 应用名称
title = PaddleOCR

# 包名
package.name = paddleocr

# 包域名
package.domain = com.ocrapp

# 源代码目录
source.dir = .

# 源代码包含的文件
source.include_exts = py,png,jpg,kv,atlas

# 主程序入口
source.main = main.py

# 版本号
version = 1.0.0

# 依赖的 Python 包
requirements = python3,kivy,pillow,paddlepaddle-tiny,paddleocr,opencv-python,numpy,pybind11

# Android 权限
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# Android API 版本
android.api = 31
android.minapi = 21
android.ndk = 23b

# Android 架构
android.archs = arm64-v8a,armeabi-v7a

# 应用图标（如果有的话）
#icon.filename = %(source.dir)s/icon.png

# 启动画面（如果有的话）
#presplash.filename = %(source.dir)s/presplash.png

# 方向
orientation = portrait

# 服务
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# Android logcat过滤器
android.logcat_filters = *:S python:D

# 如果应用不支持屏幕截图
#android.add_src = src

# Android 额外库
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-v8/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# Android 黑名单
android.gradle_dependencies = 

# Android 白名单
android.whitelist = 

# Android NDK 路径
# android.ndk_path =

# Android SDK 路径
# android.sdk_path =

# 是否跳过更新
# android.skip_update = False

# 是否接受 SDK 许可
android.accept_sdk_license = True

# Android ant 路径
# android.ant_path =

[buildozer]

# 日志级别 (0 = error only, 1 = info, 2 = debug)
log_level = 2

# 显示警告
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 二进制文件目录
bin_dir = ./bin

