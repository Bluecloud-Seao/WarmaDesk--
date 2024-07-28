import tkinter as tk
from tkinter import ttk, messagebox
import json
import sv_ttk
import winreg as reg
import sys
import os
import webbrowser

class SettingsWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 加载数据
        self.load_config_json("Config\\Config.json")

        # 加载长文本
        self.load_welcome_text("Public\\Welcome.txt")

        # 窗口基本信息
        self.title("沃玛桌宠 -设置")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = 500
        self.height = 600
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.geometry(f"{self.width}x{self.height}+{int(x)}+{int(y)}")
        self.iconbitmap(self.config['window']['icon'])

        # 程序信息
        self.python_exe = sys.executable
        self.script_path = os.path.realpath(__file__)

        try:
            sv_ttk.set_theme(self.config['window']['settings_window_theme'])
        except Exception as e:
            self.exception(e)

        # 初始化变量
        self.title_var = tk.StringVar(self, value=self.config['window']['title'])
        self.width_var = tk.StringVar(self, value=str(self.config['window']['width']))
        self.height_var = tk.StringVar(self, value=str(self.config['window']['height']))
        self.topmost_var = tk.BooleanVar(self, value=self.config['window']['topmost'])
        self.trans_var = tk.BooleanVar(self, value=self.config['window']['trans'])
        self.icon_var = tk.StringVar(self, value=self.config['window']['icon'])
        self.master_var = tk.StringVar(self, value=self.config['pets']['master'])
        self.auto_trigger_time_var = tk.StringVar(self, value=str(self.config['pets']['auto_trigger_time']))

        # 创建窗口
        self.create_notebook()
        self.create_welcome_window()
        self.create_info_window()
        self.create_window_settings()
        self.create_pets_settings()
        self.create_update_settings()

    # 加载数据函数
    def load_config_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {
                "window": {"title": "沃玛桌宠-WarmaDesk", "width": 400, "height": 400, "topmost": True, "trans": True, "icon": "icon.ico"},
                "pets": {"master": "Warma", "auto_trigger_time": 10}
            }
            with open(path, "w", encoding="utf-8") as file:
                json.dump(self.config, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件时发生错误: {e}")

    def load_welcome_text(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.welcome_text = file.read()
        except FileNotFoundError:
            self.welcome_text = "欢迎文本未找到。"
        except Exception as e:
            messagebox.showerror("错误", f"加载欢迎文本时发生错误: {e}")

    # 开机自启动函数
    def create_task(self):
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Run",
                        0, reg.KEY_SET_VALUE)

        reg.SetValueEx(key, "My Python Program", 0, reg.REG_SZ,
                    '{} "{}"'.format(self.python_exe, self.script_path))
        reg.CloseKey(key)

    def delete_task(self):
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, reg.KEY_ALL_ACCESS)
            reg.DeleteValue(key, "My Python Program")

            reg.CloseKey(key)
        except FileNotFoundError:
            pass

    # 窗口控件函数
    def create_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=5, pady=5)

        self.welcome_tap = ttk.Labelframe(notebook, text="欢迎")
        notebook.add(self.welcome_tap, text="欢迎")

        self.info_tap = ttk.Labelframe(notebook, text="信息")
        notebook.add(self.info_tap, text="信息")

        self.window_tap = ttk.Labelframe(notebook, text="窗口")
        notebook.add(self.window_tap, text="窗口")

        self.pets_tap = ttk.Labelframe(notebook, text="宠物")
        notebook.add(self.pets_tap, text="宠物")

        self.update_tab = ttk.Labelframe(notebook, text="更新")
        notebook.add(self.update_tab, text="更新")

    def create_welcome_window(self):
        title = ttk.Label(self.welcome_tap, text=f"欢迎 \^o^/", font=("微软雅黑", 20))
        text = tk.Text(self.welcome_tap, state="normal", font=("微软雅黑", 10), wrap="word")
        text.insert(tk.END, self.welcome_text)
        text['state'] = "disabled"

        scroll_bar = ttk.Scrollbar(self.welcome_tap, orient='vertical', command=text.yview)
        text.config(yscrollcommand=scroll_bar.set)

        title.pack(side="top", anchor="w", padx=10, pady=10)
        text.pack(side="top", expand=True, fill="both", padx=10, pady=10)
        scroll_bar.pack(side="right", fill="y")

    def create_info_window(self):
        info_title = ttk.Label(self.info_tap, text="程序信息", font=("微软雅黑", 20))
        info_title.pack(side="top", anchor="w", padx=10, pady=10)

        info_name_label = ttk.Label(self.info_tap, text=f"名称: {self.config['info']['name']}")
        info_name_label.pack(side="top", anchor="w", padx=10, pady=5)

        info_version_label = ttk.Label(self.info_tap, text=f"版本: {self.config['info']['version']}")
        info_version_label.pack(side="top", anchor="w", padx=10, pady=5)

        info_author_label = ttk.Label(self.info_tap, text=f"作者: {self.config['info']['author']}")
        info_author_label.pack(side="top", anchor="w", padx=10, pady=5)

        info_bilibili_label = ttk.Label(self.info_tap, text=f"Bilibili页面: {self.config['info']['bilibili_page']}")
        info_bilibili_label.pack(side="top", anchor="w", padx=10, pady=5)
        info_bilibili_label.bind("<Button-1>", self.open_bilibili_page)

        info_github_label = ttk.Label(self.info_tap, text=f"GitHub页面: {self.config['info']['github_page']}")
        info_github_label.pack(side="top", anchor="w", padx=10, pady=5)
        info_github_label.bind("<Button-1>", self.open_github_page)

        info_license_label = ttk.Label(self.info_tap, text=f"许可证: {self.config['info']['License']}")
        info_license_label.pack(side="top", anchor="w", padx=10, pady=5)

        ttk.Frame(self.info_tap, height=20).pack(side="top", fill="x")

    def create_window_settings(self):
        frame = ttk.Frame(self.window_tap)
        frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.title_var = self.create_label_entry(frame, "窗口标题:", "title", "window")
        self.width_var = self.create_label_entry(frame, "窗口宽度:","width", "window")
        self.height_var = self.create_label_entry(frame, "窗口高度:", "height", "window")
        self.topmost_var = self.create_checkbutton(frame, "窗口置顶", "topmost", "window")
        self.trans_var = self.create_checkbutton(frame, "窗口透明度", "trans", "window")
        self.icon_var = self.create_label_entry(frame, "窗口图标:", "icon", "window")

        save_button = ttk.Button(frame, text="保存设置", command=self.save_settings, style="Accent.TButton", width=20)
        save_button.pack(side="bottom", pady=20)

        autorun_button = ttk.Button(frame, text="禁用开机启动", command=self.delete_task, width=20)
        autorun_button.pack(side="bottom", pady=10)

        autorun_button = ttk.Button(frame, text="启用开机启动", command=self.create_task, width=20)
        autorun_button.pack(side="bottom", pady=10)

    def create_pets_settings(self):
        frame = ttk.Frame(self.pets_tap)
        frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.master_var = self.create_label_entry(frame, "主宠物目录名称(尽量不要改):", "master", "pets")
        self.auto_trigger_time_var = self.create_label_entry(frame, "自动触发时间 (分钟):", "auto_trigger_time", "pets")

        save_button = ttk.Button(frame, text="保存设置", command=self.save_settings, style="Accent.TButton", width=20)
        save_button.pack(side="bottom", pady=20)

    def create_update_settings(self):
        frame = ttk.Frame(self.update_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="检查更新", command=self.check_updates, style="Accent.TButton", width=100).pack(side="top", pady=20)

    def check_updates(self):
        webbrowser.open(url="https://space.bilibili.com/1858500718/dynamic", new=2)

    def create_label_entry(self, frame, label_text, option_key, setting_section):
        entry_var = tk.StringVar(value=self.config[setting_section][option_key])
        label = ttk.Label(frame, text=label_text)
        label.pack(side="top", anchor="nw", padx=5, pady=5)
        entry = ttk.Entry(frame, textvariable=entry_var)
        entry.pack(side="top", anchor="n", fill="x", expand=True)
        return entry_var

    def create_checkbutton(self, frame, text, variable_key, setting_section):
        var = tk.BooleanVar(value=self.config[setting_section][variable_key])
        check = ttk.Checkbutton(frame, text=text, variable=var, style="Switch.TCheckbutton")
        check.pack(side="top")
        return var

    def save_settings(self):
        try:
            self.config['window']['title'] = self.title_var.get()
            self.config['window']['width'] = int(self.width_var.get())
            self.config['window']['height'] = int(self.height_var.get())
            self.config['window']['topmost'] = self.topmost_var.get()
            self.config['window']['trans'] = self.trans_var.get()
            self.config['window']['icon'] = self.icon_var.get()

            self.config['pets']['master'] = self.master_var.get()
            auto_trigger_time = self.auto_trigger_time_var.get()
            if auto_trigger_time.isdigit():
                self.config['pets']['auto_trigger_time'] = int(auto_trigger_time)
            else:
                messagebox.showerror("错误", "自动触发时间必须是有效的整数。")
                return

            with open('Config\\Config.json', 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, ensure_ascii=False, indent=4)
            messagebox.showinfo("成功", "设置已保存。")
        except Exception as e:
            messagebox.showerror("错误", f"保存设置时发生错误: {e}")

    # 网页跳转函数
    def open_bilibili_page(self, event):
        webbrowser.open(url=self.config['info']['bilibili_page'], new=2)

    def open_github_page(self, event):
        webbrowser.open(url=self.config['info']['github_page'], new=2)