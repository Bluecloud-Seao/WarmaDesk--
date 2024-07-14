import tkinter as tk  
from tkinter import messagebox
from PIL import Image, ImageTk  
import webbrowser
import pystray
import winsound
from moviepy.editor import AudioFileClip
import random
from settings import SettingsWindow
# 导入子目录中的模块
import libs.TkGifWidget as TkGifWidget

  
class PetWindow(tk.Tk):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.title("Warma桌宠")  
        # 计算窗口位置和尺寸
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 200
        height = 200
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")  # 设置尺寸以及位置
        self.overrideredirect(True)  # 去除边框  
        self.attributes("-topmost", True)  # 置于顶层
        self.iconbitmap('icon.ico')  # 设置窗口图标(主要是messagebox)  
  
        # 设置背景图像  
        self.set_background_image("Image\\Background.png")  
        #设置初始图片
        self.set_warma_image("Image\\stand.png")
        # 绑定事件  
        self.bind_mouse_menu()
        self.bind_mouse_touch() 
        self.bind_mouse_move() 
  
    def set_background_image(self, image_path):  
        # 加载并调整图像大小  
        image = Image.open(image_path)  
        image = image.resize((200, 200), Image.LANCZOS)  
        photo = ImageTk.PhotoImage(image)  
    
        self.background_label = tk.Label(self, image=photo)  
        self.background_label.pack(expand=True, fill="both")  
  
        # 保持对PhotoImage的引用  
        self.background_label.image = photo 
        
    def set_warma_image(self, image_path):
        # 加载并调整图像大小  
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        self.warma_label = tk.Label(self.background_label, image=photo)
        self.warma_label.pack(expand=True, fill="both")
        
        # 绑定自动函数
        self.warma_label.after(60000, func=lambda: self.menu_eatshark(image_path="Image\\eatshark.gif", sound_path="Sound\\eatshark.wav", auto=True))
        self.warma_label.after(600000, func=lambda: self.menu_sleep(image_path="Image\\sleep.gif", sound_path="Sound\\sleep.wav", auto=True))
        
        # 保持对PhotoImage的引用  
        self.warma_label.image = photo
        
    def menu_talk(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound = random.choice(sound_path)
                sound_clip = AudioFileClip(sound)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound,  winsound.SND_ASYNC | winsound.SND_FILENAME)  #播放音频(下同)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.talk_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.talk_gif.pack(expand=True, fill="both") 
            self.talk_gif.after(int(sound_time * 1000), func=self.talk_gif.destroy)  #播放GIF动图(下同)
            
    def menu_walk(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            x = random.randint(0, self.winfo_screenwidth())
            y = random.randint(0, self.winfo_screenheight())
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.walk_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.walk_gif.pack(expand=True, fill="both") 
            self.walk_gif.after(int(sound_time * 1000), func=self.walk_gif.destroy)
            self.geometry("+{0}+{1}".format(x, y)) 
        
    def menu_sleep(self, image_path, sound_path, auto):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            if auto:
                pass
            else:
                messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.sleep_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.sleep_gif.pack(expand=True, fill="both") 
            self.sleep_gif.after(600000, func=self.sleep_gif.destroy)  # 睡觉时间依旧固定,不该时间
        
    def menu_eatshark(self, image_path, sound_path, auto):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.eatshark_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.eatshark_gif.pack(expand=True, fill="both")
            self.eatshark_gif.after(int(sound_time * 1000), func=self.eatshark_gif.destroy)
        
    def menu_nicesound(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.nicesound_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.nicesound_gif.pack(expand=True, fill="both")  
            self.nicesound_gif.after(int(sound_time * 1000), func=self.nicesound_gif.destroy)
        
    def menu_eatearth(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.eatearth_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.eatearth_gif.pack(expand=True, fill="both") 
            self.eatearth_gif.after(int(sound_time * 1000), func=self.eatearth_gif.destroy)          
        
    def menu_buy(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.buy_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.buy_gif.pack(expand=True, fill="both") 
            self.buy_gif.after(int(sound_time * 1000), func=self.buy_gif.destroy)
            
    def menu_shark(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.shark_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.shark_gif.pack(expand=True, fill="both") 
            self.shark_gif.after(int(sound_time * 1000), func=self.shark_gif.destroy)
        
    def menu_spider(self, image_path, sound_path):
        packed_widgets = self.warma_label.pack_slaves()
        if packed_widgets:
            messagebox.showwarning("Warma正忙", "Warma一次只能干一件事哦~")
        else:
            try:
                sound_clip = AudioFileClip(sound_path)
                sound_time = sound_clip.duration
                winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
            except FileNotFoundError as e:
                messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
            except RuntimeError as e:
                messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
            except Exception as e:
                messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
            self.spider_gif = TkGifWidget.AnimatedGif(master=self.warma_label, file_path=image_path, play_mode="display", loop=0)
            self.spider_gif.pack(expand=True, fill="both") 
            self.spider_gif.after(int(sound_time * 1000), func=self.spider_gif.destroy)
    
    def menu_wakeup(self, sound_path):
        try:
            winsound.PlaySound(sound_path,  winsound.SND_ASYNC | winsound.SND_FILENAME)
        except FileNotFoundError as e:
            messagebox.showerror("错误", "音频文件已丢失或损坏!请检查是不是被Warma吃掉了。错误信息\n" + str(e))
        except RuntimeError as e:
            messagebox.showerror("错误", "播放器错误,请检测程序是否正确安装。错误信息:\n" + str(e))
        except Exception as e:
            messagebox.showerror("错误", "神秘错误,疑似Warma星球的外星人入侵。依我所见不如重新安装吧!")
        try:
            self.sleep_gif.destroy()
        except AttributeError:
            messagebox.showwarning("嘿!", "Warma醒着呢!")
        
    def bilibili_warma(self):
        webbrowser.open(url="https://space.bilibili.com/53456/", new=2)  # 打开Warma主页
        
    def settings(self):
        settings_window = SettingsWindow()

    def close(self, sound_path):
        winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        self.destroy()
        
    # 小托盘功能
    def show_window(self):
        self.deiconify()
        self.icon.stop()
        
    def show_message(self):
        self.icon.notify("Warma", "啊——蜘蛛啊——")
        
    def quit_window(self):
        self.icon.stop()
        self.destroy()
  
    def unshow_window(self, image_path):  # 收入小托盘
        self.withdraw()
        menu = (pystray.MenuItem(text="启动", action=self.show_window, default=True),
                pystray.MenuItem(text="啊——", action=self.show_message),
                pystray.MenuItem(text="退出", action=self.quit_window)
        )
        image = Image.open(image_path)
        self.icon = pystray.Icon("Warma桌宠", image, "nia~", menu)
        self.icon.run()
  
    def show_menu(self, event):  
        menu = tk.Menu(self, tearoff=0)  
        menu.add_command(label="说话", command=lambda: self.menu_talk(image_path="Image\\talk.gif", sound_path=["Sound\\talk_1.wav", "Sound\\talk_2.wav", "Sound\\talk_3.wav"]))
        menu.add_command(label="走路", command=lambda: self.menu_walk(image_path="Image\\walk.gif", sound_path="Sound\\walk.wav"))
        menu.add_command(label="睡觉", command=lambda: self.menu_sleep(image_path="Image\\sleep.gif", sound_path="Sound\\sleep.wav", auto=False))
        menu.add_separator()
        menu.add_command(label="尝鲨", command=lambda: self.menu_eatshark(image_path="Image\\eatshark.gif", sound_path="Sound\\eatshark.wav", auto=False))
        menu.add_command(label="吹灭人器", command=lambda: self.menu_nicesound(image_path="Image\\nicesound.gif", sound_path="Sound\\nicesound.wav"))
        menu.add_command(label="吃地球", command=lambda: self.menu_eatearth(image_path="Image\\eatearth.gif", sound_path="Sound\\eatearth.wav"))
        menu.add_command(label="买吗?", command=lambda: self.menu_buy(image_path="Image\\buy.gif", sound_path="Sound\\buy.wav"))
        menu.add_separator()
        menu.add_command(label="小鲨鱼", command=lambda: self.menu_shark(image_path="Image\\shark.gif", sound_path="Sound\\shark.wav"))
        menu.add_command(label="蜘蛛啊!", command=lambda: self.menu_spider(image_path="Image\\spider.gif", sound_path="Sound\\spider.wav"))
        menu.add_separator()
        menu.add_command(label="看Warma视频", command=self.bilibili_warma)
        menu.add_separator()
        menu.add_command(label="设置", command=self.settings)
        menu.add_separator()
        menu.add_command(label="叫醒Warma", command=lambda: self.menu_wakeup(sound_path="Sound\\talk_1.wav"))
        menu.add_command(label="收入小托盘", command=lambda: self.unshow_window(image_path="Image\\icon.png"))
        menu.add_command(label="再见", command=lambda: self.close(sound_path="Sound\\bye.wav")) 
        menu.post(event.x_root, event.y_root)  
  
    def bind_mouse_menu(self):  
        # 绑定右键点击事件来显示菜单  
        self.bind("<Button-3>", self.show_menu)  
        
    def bind_mouse_touch_event(self, event):
        self.start_x = self.winfo_pointerx() - self.winfo_rootx()
        self.start_y = self.winfo_pointery() - self.winfo_rooty()
        
    def bind_mouse_touch(self):
        self.bind("<Button-1>", self.bind_mouse_touch_event)
        
    def bind_mouse_move_event(self, event):
        self.deltax = self.winfo_pointerx() - self.start_x
        self.deltay = self.winfo_pointery() - self.start_y
        self.geometry("+{0}+{1}".format(self.deltax, self.deltay))
        
    def bind_mouse_move(self):
        self.bind("<B1-Motion>", self.bind_mouse_move_event)

if __name__ == "__main__":  
    app = PetWindow()  
    app.mainloop()