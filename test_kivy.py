"""
Kivy 测试程序
用于在本地测试 Kivy 应用是否正常运行（不需要构建 APK）
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        label = Label(
            text='Kivy 测试成功！\n环境配置正常',
            font_size='24sp'
        )
        
        button = Button(
            text='点击测试',
            size_hint=(1, 0.2),
            font_size='18sp'
        )
        
        def on_button_click(instance):
            label.text = 'Kivy 工作正常！\n可以开始构建 Android 应用了'
        
        button.bind(on_press=on_button_click)
        
        layout.add_widget(label)
        layout.add_widget(button)
        
        return layout


if __name__ == '__main__':
    print("="*50)
    print("Kivy 测试程序")
    print("="*50)
    print("\n如果窗口正常打开并且按钮可以点击，")
    print("说明 Kivy 环境配置正确。\n")
    print("可以继续构建 Android APK。")
    print("="*50)
    
    TestApp().run()

