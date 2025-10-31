"""
PaddleOCR Android 版本
使用 Kivy 框架构建的移动端 OCR 应用
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import os
import tempfile


class OCRApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ocr_engine = None
        self.current_image_path = None
        self.camera = None
        
    def build(self):
        # 设置窗口背景色
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # 主布局
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        title_layout = BoxLayout(size_hint=(1, 0.1), padding=5)
        with title_layout.canvas.before:
            Color(0.098, 0.463, 0.824, 1)  # #1976D2
            self.title_rect = Rectangle(size=title_layout.size, pos=title_layout.pos)
        title_layout.bind(size=self._update_title_rect, pos=self._update_title_rect)
        
        title = Label(
            text='[b]PaddleOCR 移动版[/b]',
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        title_layout.add_widget(title)
        self.main_layout.add_widget(title_layout)
        
        # 按钮区域
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        # 拍照按钮
        self.camera_btn = Button(
            text='📷 拍照',
            font_size='16sp',
            background_color=(0.3, 0.7, 0.3, 1),
            background_normal=''
        )
        self.camera_btn.bind(on_press=self.open_camera)
        btn_layout.add_widget(self.camera_btn)
        
        # 选择图片按钮
        self.gallery_btn = Button(
            text='🖼️ 相册',
            font_size='16sp',
            background_color=(0.2, 0.6, 0.9, 1),
            background_normal=''
        )
        self.gallery_btn.bind(on_press=self.open_gallery)
        btn_layout.add_widget(self.gallery_btn)
        
        # 识别按钮
        self.recognize_btn = Button(
            text='🚀 识别',
            font_size='16sp',
            background_color=(1, 0.6, 0, 1),
            background_normal=''
        )
        self.recognize_btn.bind(on_press=self.recognize_image)
        btn_layout.add_widget(self.recognize_btn)
        
        # 复制按钮
        self.copy_btn = Button(
            text='📋 复制',
            font_size='16sp',
            background_color=(0.13, 0.59, 0.95, 1),
            background_normal=''
        )
        self.copy_btn.bind(on_press=self.copy_result)
        btn_layout.add_widget(self.copy_btn)
        
        self.main_layout.add_widget(btn_layout)
        
        # 图片预览区域
        preview_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.35))
        preview_label = Label(
            text='图片预览',
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0, 0, 0, 1)
        )
        preview_layout.add_widget(preview_label)
        
        self.image_preview = Image(
            source='',
            size_hint=(1, 0.9),
            allow_stretch=True,
            keep_ratio=True
        )
        preview_layout.add_widget(self.image_preview)
        self.main_layout.add_widget(preview_layout)
        
        # 识别结果区域
        result_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        result_label = Label(
            text='识别结果',
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0, 0, 0, 1)
        )
        result_layout.add_widget(result_label)
        
        # 滚动文本区域
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.result_text = TextInput(
            text='请选择图片或拍照，然后点击"识别"按钮',
            multiline=True,
            readonly=True,
            font_size='14sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        scroll_view.add_widget(self.result_text)
        result_layout.add_widget(scroll_view)
        
        self.main_layout.add_widget(result_layout)
        
        # 状态栏
        self.status_label = Label(
            text='就绪 | PaddleOCR 中文识别',
            size_hint=(1, 0.05),
            font_size='12sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        self.main_layout.add_widget(self.status_label)
        
        return self.main_layout
    
    def _update_title_rect(self, instance, value):
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size
    
    def open_camera(self, instance):
        """打开相机拍照"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            
            # 检查并请求相机权限
            if not check_permission(Permission.CAMERA):
                request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])
        
        # 创建相机弹窗
        camera_layout = BoxLayout(orientation='vertical')
        
        self.camera = Camera(play=True, resolution=(640, 480))
        camera_layout.add_widget(self.camera)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        capture_btn = Button(text='拍照', background_color=(0.3, 0.7, 0.3, 1))
        cancel_btn = Button(text='取消', background_color=(0.7, 0.3, 0.3, 1))
        
        btn_layout.add_widget(capture_btn)
        btn_layout.add_widget(cancel_btn)
        camera_layout.add_widget(btn_layout)
        
        self.camera_popup = Popup(
            title='拍照',
            content=camera_layout,
            size_hint=(0.9, 0.9)
        )
        
        capture_btn.bind(on_press=self.capture_photo)
        cancel_btn.bind(on_press=self.camera_popup.dismiss)
        
        self.camera_popup.open()
    
    def capture_photo(self, instance):
        """捕获照片"""
        if self.camera:
            # 保存照片到临时文件
            temp_dir = tempfile.gettempdir()
            photo_path = os.path.join(temp_dir, 'ocr_photo.png')
            self.camera.export_to_png(photo_path)
            
            # 更新图片预览
            self.current_image_path = photo_path
            self.image_preview.source = photo_path
            self.result_text.text = f'已拍照: {os.path.basename(photo_path)}\n点击"识别"按钮开始识别'
            self.status_label.text = f'已加载: {os.path.basename(photo_path)}'
            
            # 关闭相机
            self.camera_popup.dismiss()
    
    def open_gallery(self, instance):
        """打开图库选择图片"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            
            # 检查并请求存储权限
            if not check_permission(Permission.READ_EXTERNAL_STORAGE):
                request_permissions([Permission.READ_EXTERNAL_STORAGE])
        
        # 创建文件选择器弹窗
        file_chooser = FileChooserIconView(
            filters=['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif'],
            path='/sdcard/DCIM/' if platform == 'android' else os.path.expanduser('~')
        )
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        select_btn = Button(text='选择', background_color=(0.3, 0.7, 0.3, 1))
        cancel_btn = Button(text='取消', background_color=(0.7, 0.3, 0.3, 1))
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        gallery_layout = BoxLayout(orientation='vertical')
        gallery_layout.add_widget(file_chooser)
        gallery_layout.add_widget(btn_layout)
        
        self.gallery_popup = Popup(
            title='选择图片',
            content=gallery_layout,
            size_hint=(0.9, 0.9)
        )
        
        def select_file(instance):
            if file_chooser.selection:
                image_path = file_chooser.selection[0]
                self.current_image_path = image_path
                self.image_preview.source = image_path
                self.result_text.text = f'已选择: {os.path.basename(image_path)}\n点击"识别"按钮开始识别'
                self.status_label.text = f'已加载: {os.path.basename(image_path)}'
                self.gallery_popup.dismiss()
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=self.gallery_popup.dismiss)
        
        self.gallery_popup.open()
    
    def init_ocr(self):
        """初始化 OCR 引擎"""
        if self.ocr_engine is None:
            try:
                self.status_label.text = '正在初始化 PaddleOCR...'
                from paddleocr import PaddleOCR
                self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)
                self.status_label.text = '就绪 | PaddleOCR 已初始化'
                return True
            except Exception as e:
                self.show_popup('错误', f'初始化失败:\n{str(e)}')
                self.status_label.text = '初始化失败'
                return False
        return True
    
    def recognize_image(self, instance):
        """识别图片中的文字"""
        if not self.current_image_path:
            self.show_popup('提示', '请先选择图片或拍照')
            return
        
        if not os.path.exists(self.current_image_path):
            self.show_popup('错误', '图片文件不存在')
            return
        
        # 初始化 OCR
        if not self.init_ocr():
            return
        
        try:
            self.result_text.text = '🔍 正在识别...\n请稍候...'
            self.status_label.text = '识别中...'
            
            # 延迟执行 OCR，让 UI 先更新
            Clock.schedule_once(lambda dt: self._do_ocr(), 0.1)
            
        except Exception as e:
            self.show_popup('错误', f'识别失败:\n{str(e)}')
            self.status_label.text = '识别失败'
    
    def _do_ocr(self):
        """执行 OCR 识别"""
        try:
            result = self.ocr_engine.ocr(self.current_image_path, cls=True)
            
            if result and len(result) > 0:
                lines = result[0]
                
                if lines:
                    text_lines = []
                    confidences = []
                    
                    output = '=' * 40 + '\n✅ 识别成功!\n' + '=' * 40 + '\n\n'
                    
                    for idx, line in enumerate(lines, 1):
                        box, (text, confidence) = line
                        text_lines.append(text)
                        confidences.append(confidence)
                        output += f'{idx:2d}. {text} ({confidence:.1%})\n'
                    
                    avg_conf = sum(confidences) / len(confidences)
                    
                    output += '\n' + '-' * 40 + '\n📄 完整文本:\n' + '-' * 40 + '\n\n'
                    output += '\n'.join(text_lines)
                    output += f'\n\n' + '=' * 40 + '\n'
                    output += f'📊 识别行数: {len(text_lines)} | 平均置信度: {avg_conf:.1%}\n'
                    
                    self.result_text.text = output
                    self.status_label.text = f'识别完成 | {len(text_lines)}行 | {avg_conf:.1%}'
                    
                    # 保存完整文本用于复制
                    self.last_result = '\n'.join(text_lines)
                else:
                    self.result_text.text = '❌ 未识别到文字'
                    self.status_label.text = '未识别到文字'
            else:
                self.result_text.text = '❌ 未识别到文字'
                self.status_label.text = '未识别到文字'
                
        except Exception as e:
            self.result_text.text = f'❌ 识别出错:\n{str(e)}'
            self.status_label.text = '识别错误'
    
    def copy_result(self, instance):
        """复制识别结果"""
        if hasattr(self, 'last_result') and self.last_result:
            try:
                # Android 剪贴板
                if platform == 'android':
                    from android import mActivity
                    from jnius import autoclass, cast
                    
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Context = autoclass('android.content.Context')
                    ClipboardManager = autoclass('android.content.ClipboardManager')
                    ClipData = autoclass('android.content.ClipData')
                    
                    clipboard = cast(ClipboardManager, 
                                   mActivity.getSystemService(Context.CLIPBOARD_SERVICE))
                    clip = ClipData.newPlainText('OCR Result', self.last_result)
                    clipboard.setPrimaryClip(clip)
                else:
                    # 桌面平台
                    from kivy.core.clipboard import Clipboard
                    Clipboard.copy(self.last_result)
                
                self.show_popup('成功', '识别结果已复制到剪贴板')
                self.status_label.text = '已复制到剪贴板'
            except Exception as e:
                self.show_popup('错误', f'复制失败:\n{str(e)}')
        else:
            self.show_popup('提示', '没有可复制的内容')
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, size_hint=(1, 0.8))
        popup_btn = Button(text='确定', size_hint=(1, 0.2))
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_btn)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    OCRApp().run()

