import tkinter as tk
from tkinter import ttk
import time
import sv_ttk
import webbrowser
import os

class SettingsWindow(tk.Toplevel):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Warma桌宠设置")
        # 计算窗口位置和尺寸
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 1000
        height = 750
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")  # 设置尺寸以及位置
        self.overrideredirect(True)  # 去除边框
        sv_ttk.use_light_theme()  # 运用sv_ttk主题
        
        # 渲染窗口
        self.window()
        self.main()

    # 事件函数    
    def title_mouse_touch_event(self, event):  # 记录鼠标按下标题
        self.start_x = self.winfo_pointerx() - self.winfo_rootx()
        self.start_y = self.winfo_pointery() - self.winfo_rooty()
        
    def title_mouse_move_event(self, event):  # 记录鼠标移动
        self.deltax = self.winfo_pointerx() - self.start_x
        self.deltay = self.winfo_pointery() - self.start_y
        self.geometry("+{0}+{1}".format(self.deltax, self.deltay))
        
    def fullscreen_event(self, event):  #窗口最大化
        self.overrideredirect(False)
        self.attributes("-fullscreen", True)
        
    def unfullscreen_event(self, event):
        self.overrideredirect(True)
        self.attributes("-fullscreen", False)
        
    def exit_event(self, event):
        self.window_title_button_exit.bg = "#EC0000"
        time.sleep(0.1)
        self.destroy()
        
    def resize_event(self, event):
        self.geometry("{0}x{1}".format(self.winfo_width() - 10, self.winfo_height() - 10))

    def update_event(self, event):
        webbrowser.open(url="https://space.bilibili.com/1858500718/dynamic", new=2)
        self.destroy()

    # Command调用函数
    def button_visit(self):
        webbrowser.open(url="https://space.bilibili.com/1858500718", new=2)

    def button_imagefiles(self):
        os.startfile("Image\\")

    def button_soundfiles(self):
        os.startfile("Sound\\")

    # 窗口函数    
    def window(self):
        window_background = tk.Frame(self, height=750, width=1000, bg="#61bbd1")
        window_background.pack(expand=True, fill="both")
        # 窗口背景
        window_title = tk.Frame(window_background, height=50, width=1000, bg="#61bbd1")
        window_title.pack(side="top", anchor="n" ,expand=True, fill="x")
        window_title.pack_propagate(False)
        window_title.bind("<Button-1>", self.title_mouse_touch_event)
        window_title.bind("<B1-Motion>", self.title_mouse_move_event)
        # 窗口标题栏
        window_title_labelframe = tk.Frame(window_title, height=50, width=80, bg="#61bbd1")
        window_title_labelframe.pack(side="left", anchor="w", expand=True, fill="y", padx=10, pady=10)
        # 标题容器
        window_title_label = tk.Label(window_title_labelframe, text="Warma桌宠", font=("微软雅黑", 12), bg="#61bbd1")
        window_title_label.pack(expand=True, fill="both", padx=5, pady=5)
        window_title_label.bind("<Button-1>", self.fullscreen_event)
        window_title_label.bind("<Button-3>", self.unfullscreen_event)
        # 窗口标题
        window_title_buttonframe = tk.Frame(window_title, height=50, width=100, bg="#61bbd1")
        window_title_buttonframe.pack(side="right", anchor="e", expand=True, fill="y", padx=10, pady=10)
        # 标题按钮容器
        self.window_title_button_exit = tk.Label(window_title_buttonframe, text="X", font=("微软雅黑", 15, "bold"), bg="#61bbd1")
        self.window_title_button_exit.pack(expand=True, fill="both", padx=5, pady=5)
        self.window_title_button_exit.bind("<Button-1>", self.exit_event)
        self.window_title_button_exit.bind("<Button-3>", self.resize_event)
        # 标题按钮
        self.window_main = tk.Frame(window_background, height=700, width=1000)
        self.window_main.pack(side="bottom", anchor="s", expand=True, fill="both", padx=10, pady=10)
        self.window_main.pack_propagate(False)
        # 窗口主体
        
    def main(self):
        notebook = ttk.Notebook(self.window_main)
        notebook.pack(expand=True, fill="both", padx=5, pady=5)
        # 标签栏

        tab_tips = ttk.Labelframe(notebook, text="程序介绍", height=750, width=1000)
        notebook.add(tab_tips, text="程序介绍")
        # 程序介绍标签
        tab_tips_titleframe = tk.Frame(tab_tips, height=50, width=1000)
        tab_tips_titleframe.pack(side="top", anchor="n", padx=10, pady=10)
        tab_tips_titleframe.pack_propagate(False)
        # 介绍标题容器
        tab_tips_title = tk.Label(tab_tips_titleframe, text="使用小贴士", font=("微软雅黑", 20))
        tab_tips_title.pack(side="left", anchor="w", expand=True, fill="y")
        # 程序介绍标题
        tab_tips_mainframe = tk.Frame(tab_tips, height=650, width=1000)
        tab_tips_mainframe.pack(side="top", anchor="n", expand=True, fill="x", padx=10, pady=10)
        # 程序主文本容器
        tab_tips_maintext = "欢迎使用Warma桌宠！非常感谢您选择我们！特别鸣谢B站UP主 @FunTime工作室 提供灵感\n1) 主窗口（Warma窗口）\n    鼠标左键长按Warma并拖动可移动Warma，右键可打开功能菜单——播放动画或执行其他操作。\n2) 设置窗口\n    设置窗口标题栏为作者自行编写，因此操作方法与传统窗口不同。鼠标左键点击窗口标题可全屏窗口（含有标题变大的BUG），右键即可恢复大小。鼠标左键长按顶端蓝色区域并拖动可更改窗口位置（与传统窗口无异）。鼠标左键点击右上角“X”可关闭窗口，右键点击则缩小窗口。\n3) 小托盘\n    Warma窗口右键菜单中选择“收入小托盘”即可把程序收入系统托盘（免打扰模式）。收入小托盘后程序图标就是Warma，右键即可打开菜单。"
        tab_tips_main = tk.Message(tab_tips_mainframe, text=tab_tips_maintext, font=("微软雅黑", 12), width=920)
        tab_tips_main.pack(side="top", anchor="n", expand=True, fill="both", padx=10, pady=10)
        # 程序主文本
        tab_tips_buttonframe_about = tk.Frame(tab_tips, height=50, width=1000)
        tab_tips_buttonframe_about.pack(side="bottom", anchor="s", expand=True, fill="x", padx=10, pady=10)
        # 按钮容器
        tab_tips_button_about = ttk.Button(tab_tips_buttonframe_about, text="关于作者", width=20, style="Accent.TButton", command=self.button_visit)
        tab_tips_button_about.pack(side="right", anchor="e", expand=True, fill="y", padx=5, pady=5)
        # “关于作者”按钮

        tab_images = ttk.Labelframe(notebook, text="更改图像", height=750, width=1000)
        notebook.add(tab_images, text="更改图像")
        # 更改图像标签
        tab_images_titleframe = tk.Frame(tab_images, height=50, width=1000)
        tab_images_titleframe.pack(side="top", anchor="n", padx=10, pady=10)
        tab_images_titleframe.pack_propagate(False)
        # 标题容器
        tab_images_title = tk.Label(tab_images_titleframe, text="更改图像", font=("微软雅黑", 20))
        tab_images_title.pack(side="left", anchor="w", expand=True, fill="y")        
        # 标题
        tab_images_mainframe = tk.Frame(tab_images, height=700, width=1000)
        tab_images_mainframe.pack(side="top", anchor="n", expand=True, fill="both", padx=10, pady=10)
        # 主容器
        tab_images_label_text = "欲更换图像，请点击下方按钮打开图像文件夹，并将目标文件(必须为.gif文件)更名为目标文件名后粘贴进文件夹即可。(Warma这么可爱你不会想换掉她吧)"
        tab_images_label = tk.Label(tab_images_mainframe, text=tab_images_label_text, font=("微软雅黑", 10))
        tab_images_label.pack(side="top", anchor="w", padx=10, pady=10)
        # 文本(不知如何注释)
        tab_images_button_changefiles = ttk.Button(tab_images_mainframe, text="打开图像文件夹", width=20, style="Accent.TButton", command=self.button_imagefiles)
        tab_images_button_changefiles.pack(side="top", anchor="w", padx=10, pady=10)
        # 按钮

        tab_sound = ttk.Labelframe(notebook, text="更改音频", height=750, width=1000)
        notebook.add(tab_sound, text="更改音频")
        # 更改音频标签
        tab_sound_titleframe = tk.Frame(tab_sound, height=50, width=1000)
        tab_sound_titleframe.pack(side="top", anchor="n", padx=10, pady=10)
        tab_sound_titleframe.pack_propagate(False)
        # 标题容器
        tab_sound_title = tk.Label(tab_sound_titleframe, text="更改音频", font=("微软雅黑", 20))
        tab_sound_title.pack(side="left", anchor="w", expand=True, fill="y")        
        # 标题
        tab_sound_mainframe = tk.Frame(tab_sound, height=700, width=1000)
        tab_sound_mainframe.pack(side="top", anchor="n", expand=True, fill="both", padx=10, pady=10)
        # 主容器
        tab_sound_label_text = "欲更换音频，请点击下方按钮打开音频文件夹，并将目标文件(必须为.wav文件)更名为目标文件名后粘贴进文件夹即可。(Warma这么可爱你不会想换掉她吧)"
        tab_sound_label = tk.Label(tab_sound_mainframe, text=tab_sound_label_text, font=("微软雅黑", 10))
        tab_sound_label.pack(side="top", anchor="w", padx=10, pady=10)
        # 文本(不知如何注释)
        tab_sound_button_changefiles = ttk.Button(tab_sound_mainframe, text="打开音频文件夹", width=20, style="Accent.TButton", command=self.button_soundfiles)
        tab_sound_button_changefiles.pack(side="top", anchor="w", padx=10, pady=10)
        # 按钮

        tab_update = ttk.Labelframe(notebook, text="点击任意处以更新", height=750, width=1000)
        tab_update.bind("<Button-1>", self.update_event)
        notebook.add(tab_update, text="更新")
        # 更新标签
        tab_update_label = tk.Label(tab_update, text="点击任意处更新", font=("微软雅黑", 15), foreground="#DDDDDD")
        tab_update_label.pack()
        # 更新标签中的文本(懒得写布局了)