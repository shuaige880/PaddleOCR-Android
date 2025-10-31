"""
PaddleOCR 识别系统
中文识别准确率 97%+，远超Tesseract
"""
import os



def create_gui():
    """创建PaddleOCR图形界面"""
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext
    from PIL import Image, ImageTk
    
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        print("请先安装 PaddleOCR:")
        print("pip install paddlepaddle paddleocr")
        return
    
    class PaddleOCRApp:
        def __init__(self, root):
            self.root = root
            self.root.title("PaddleOCR 识别系统")
            self.root.geometry("1100x800")
            
            self.image_path = None
            self.pil_image = None
            self.ocr_engine = None
            
            self.setup_ui()
        
        def setup_ui(self):
            # 标题
            title_frame = tk.Frame(self.root, bg="#1976D2", height=60)
            title_frame.pack(fill=tk.X)
            title_frame.pack_propagate(False)
            
            tk.Label(title_frame, text="🎯 PaddleOCR 识别系统", 
                    font=("Arial", 18, "bold"), bg="#1976D2", fg="white").pack(pady=15)
            
            # 按钮
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(pady=15)
            
            tk.Button(btn_frame, text="📁 打开图片", command=self.open_image,
                     width=12, height=2, bg="#4CAF50", fg="white",
                     font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="🚀 开始识别", command=self.recognize,
                     width=12, height=2, bg="#FF9800", fg="white",
                     font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="📋 复制结果", command=self.copy_result,
                     width=12, height=2, bg="#2196F3", fg="white",
                     font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="🗑️ 清空", command=self.clear,
                     width=12, height=2, bg="#9E9E9E", fg="white",
                     font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
            
            # 提示
            tip_frame = tk.Frame(self.root, bg="#E8F5E9", height=50)
            tip_frame.pack(fill=tk.X, padx=10, pady=5)
            tip_frame.pack_propagate(False)
            
            # 图片预览
            img_frame = tk.LabelFrame(self.root, text="📷 图片预览", 
                                     font=("Arial", 10, "bold"))
            img_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            self.image_label = tk.Label(img_frame, bg="#f0f0f0", 
                                       text="请打开图片", font=("Arial", 12), fg="#999")
            self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 识别结果
            result_frame = tk.LabelFrame(self.root, text="📝 识别结果", 
                                        font=("Arial", 10, "bold"))
            result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            self.text_area = scrolledtext.ScrolledText(result_frame, height=12, 
                                                       width=100, font=("Consolas", 10), 
                                                       wrap=tk.WORD)
            self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 状态栏
            self.status_bar = tk.Label(self.root, text="就绪 | 准确率: 97%+", 
                                      bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                                      font=("Arial", 9))
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def init_ocr(self):
            """初始化OCR引擎"""
            if self.ocr_engine is None:
                self.status_bar.config(text="正在初始化PaddleOCR引擎...")
                self.root.update()
                self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch')
                self.status_bar.config(text="就绪 | PaddleOCR引擎已初始化")
        
        def open_image(self):
            path = filedialog.askopenfilename(
                title="选择图片",
                filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                          ("所有文件", "*.*")]
            )
            
            if path:
                try:
                    self.image_path = path
                    self.pil_image = Image.open(path)
                    self.display_image()
                    
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, f"✅ 已加载图片\n")
                    self.text_area.insert(tk.END, f"   文件: {os.path.basename(path)}\n")
                    self.text_area.insert(tk.END, f"   尺寸: {self.pil_image.size[0]} × {self.pil_image.size[1]}\n\n")
                    self.text_area.insert(tk.END, "点击 '🚀 开始识别' 使用PaddleOCR识别")
                    
                    self.status_bar.config(text=f"已加载: {os.path.basename(path)}")
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开图片:\n{str(e)}")
        
        def display_image(self):
            if self.pil_image:
                display_img = self.pil_image.copy()
                display_img.thumbnail((1000, 400), Image.Resampling.LANCZOS)
                
                self.photo = ImageTk.PhotoImage(display_img)
                self.image_label.config(image=self.photo, text="", bg="#f0f0f0")
        
        def recognize(self):
            if not self.image_path:
                messagebox.showwarning("警告", "请先打开图片")
                return
            
            try:
                # 初始化OCR引擎
                self.init_ocr()
                
                # 清空结果
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "🔍 正在使用PaddleOCR识别...\n请稍候...\n")
                self.status_bar.config(text="识别中...")
                self.root.update()
                
                # 执行OCR
                result = self.ocr_engine.ocr(self.image_path)
                
                # 显示结果
                self.text_area.delete(1.0, tk.END)
                
                if result and len(result) > 0:
                    ocr_result = result[0]
                    
                    # OCRResult是一个字典，包含 'rec_texts' 和 'rec_scores' 键
                    if isinstance(ocr_result, dict) and 'rec_texts' in ocr_result and 'rec_scores' in ocr_result:
                        texts = ocr_result['rec_texts']
                        scores = ocr_result['rec_scores']
                        
                        if texts and len(texts) > 0:
                            self.text_area.insert(tk.END, "=" * 80 + "\n")
                            self.text_area.insert(tk.END, "✅ 识别成功!\n")
                            self.text_area.insert(tk.END, "=" * 80 + "\n\n")
                            
                            # 显示每行识别结果
                            for idx, (text, score) in enumerate(zip(texts, scores), 1):
                                self.text_area.insert(tk.END, f"{idx:2d}. {text}  (置信度: {score:.1%})\n")
                            
                            # 计算平均置信度
                            avg_confidence = sum(scores) / len(scores) if scores else 0
                            
                            # 显示完整文本
                            self.text_area.insert(tk.END, "\n" + "-" * 80 + "\n")
                            self.text_area.insert(tk.END, "📄 完整文本:\n")
                            self.text_area.insert(tk.END, "-" * 80 + "\n\n")
                            self.text_area.insert(tk.END, '\n'.join(texts))
                            self.text_area.insert(tk.END, "\n\n" + "=" * 80 + "\n")
                            self.text_area.insert(tk.END, f"📊 识别行数: {len(texts)} | 平均置信度: {avg_confidence:.1%}\n")
                            
                            self.status_bar.config(text=f"识别完成 | 行数: {len(texts)} | 置信度: {avg_confidence:.1%}")
                            messagebox.showinfo("成功", f"识别完成!\n识别了 {len(texts)} 行文字\n平均置信度: {avg_confidence:.1%}")
                        else:
                            self.text_area.insert(tk.END, "❌ 未识别到文字\n")
                            self.status_bar.config(text="未识别到文字")
                    else:
                        self.text_area.insert(tk.END, "❌ 无法解析OCR结果对象\n")
                        self.text_area.insert(tk.END, f"对象类型: {type(ocr_result)}\n")
                        if isinstance(ocr_result, dict):
                            self.text_area.insert(tk.END, f"可用键: {list(ocr_result.keys())}\n")
                        self.status_bar.config(text="格式错误")
                else:
                    self.text_area.insert(tk.END, "❌ 未识别到文字\n")
                    self.status_bar.config(text="未识别到文字")
                
            except Exception as e:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f"❌ 识别出错:\n{str(e)}\n")
                self.status_bar.config(text="识别错误")
                messagebox.showerror("错误", f"识别失败:\n{str(e)}")
        
        def copy_result(self):
            try:
                text = self.text_area.get(1.0, tk.END)
                
                # 提取完整文本部分
                if "完整文本:" in text:
                    parts = text.split("完整文本:")
                    if len(parts) > 1:
                        result_part = parts[1].split("=" * 80)[0].strip()
                        result = result_part.replace("-" * 80, "").strip()
                    else:
                        result = text.strip()
                else:
                    result = text.strip()
                
                if result:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(result)
                    messagebox.showinfo("成功", "识别结果已复制到剪贴板")
                    self.status_bar.config(text="已复制到剪贴板")
                else:
                    messagebox.showwarning("警告", "没有可复制的内容")
            except Exception as e:
                messagebox.showerror("错误", f"复制失败:\n{str(e)}")
        
        def clear(self):
            self.text_area.delete(1.0, tk.END)
            if self.pil_image:
                self.text_area.insert(tk.END, "已清空。点击 '🚀 开始识别' 重新识别...")
            self.status_bar.config(text="已清空")
    
    root = tk.Tk()
    app = PaddleOCRApp(root)
    root.mainloop()


if __name__ == "__main__":
    import sys
    
    
   
    
    print("\n启动图形界面...")
    create_gui()

