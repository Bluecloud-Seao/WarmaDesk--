import tkinter as tk  
from tkinter import messagebox
from PIL import Image, ImageTk  
import winsound
from moviepy.editor import AudioFileClip
import random
import json
import pystray
import os
import sys
from settings import SettingsWindow
# 导入子目录中的模块
import libs.TkGifWidget as TkGifWidget
  
class PetWindow(tk.Tk):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        # 透明颜色
        self.TRANSCOLOUR = "gray"

        #初始化动画组件
        self.animation = None

        # 初始化呼吸动画
        self.breathing_factor = 0.008  # 呼吸效果的缩放比例因子
        self.breathing_speed = 550  # 注意!数值越小，动画越快

        # 加载数据
        self.load_config_json("Config\\Config.json")  # 公共数据
        self.load_pet_info_json(f"Pets\\{self.config['pets']['master']}\\Config\\Info.json")
        self.load_pet_menu_json(f"Pets\\{self.config['pets']['master']}\\Config\\Menu.json")

        # 窗口基本信息
        self.title(self.config['window']['title'])  
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = self.config['window']['width']
        self.height = self.config['window']['height']
        x = screen_width - self.width - 10
        y = screen_height - self.height -10
        self.geometry(f"{self.width}x{self.height}+{int(x)}+{int(y)}")  # 设置尺寸以及位置
        self.overrideredirect(self.config['window']['no_header'])  # 去除边框  
        self.attributes("-topmost", self.config['window']['topmost'])  # 置于顶层
        self.iconbitmap(self.config['window']['icon'])  # 设置窗口图标(主要是messagebox)
        self.wm_attributes("-transparentcolor", self.TRANSCOLOUR)  
        if self.config['window']['trans']:
            self.configure(background=self.TRANSCOLOUR)  # 窗口背景透明

        # 定时播放自动动画
        auto_trigger_time = self.config['pets']['auto_trigger_time']
        self.after(auto_trigger_time * 60 * 1000, func=self.auto_animation_play)

        # 加载宠物名称函数
        self.load_pet_names("Pets", "Config", "Info.json")

        # 加载主图片
        self.set_pet_image()

        # 绑定事件函数
        self.bind_mouse_touch() 
        self.bind_mouse_move() 
        self.bind_mouse_menu()
 
    # 加载数据函数
    def load_config_json(self, config_path):
        try:
            with open(config_path, 'r', encoding="utf-8") as file:
                self.config = json.load(file)  
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

    def load_pet_info_json(self, config_path):
        try:
            with open(config_path, 'r', encoding="utf-8") as file:
                self.pet_info_config = json.load(file)  
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

    def load_pet_menu_json(self, config_path):
        try:
            with open(config_path, 'r', encoding="utf-8") as file:
                self.pet_menu_config = json.load(file)  
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

    def load_pet_names(self, pets_path, config_path, info_filename):
        self.pet_names = []

        # 遍历 Pets 文件夹下的所有文件夹
        for pet_folder in os.listdir(pets_path):
            pet_folder_path = os.path.join(pets_path, pet_folder)

            if os.path.isdir(pet_folder_path):
                config_folder_path = os.path.join(pet_folder_path, config_path)
                if os.path.isdir(config_folder_path):
                    info_file_path = os.path.join(config_folder_path, info_filename)
                    if os.path.isfile(info_file_path):
                        try:
                            with open(info_file_path, 'r', encoding='utf-8') as info_file:
                                info_data = json.load(info_file)
                                # 获取 pet_info 下的 name 项并添加到列表中
                                pet_name = info_data.get('pet_info', {}).get('name')
                                if pet_name:
                                    self.pet_names.append(pet_name)
                        except json.JSONDecodeError as e:
                            self.json_decode_error(e)

    # 错误处理函数
    def file_not_found_error(self, error):
        messagebox.showerror("错误", f"文件丢失!疑似被沃星人偷走! Error:{str(error)}")

    def json_decode_error(self, error):
        messagebox.showerror("错误", f"配置文件错误!是不是改文件时写错了? Error:{str(error)}")

    def type_error(self, error):
        messagebox.showerror("错误", f"格式处理错误,请检查配置文件是否正确! Error:{str(error)}")

    def runtime_error(self, error):
        messagebox.showerror("错误", f"音频播放器错误!请检查沃玛是否正确入住电脑。 Error:{str(error)}")

    def be_busy_warning(self):
        messagebox.showwarning("嗨!", "沃玛只可以做一件事哦!")

    def attribute_error(self, error):
        messagebox.showwarning("嗨", f"沃玛什么事也没干!")

    def restart_warning(self):
        restart = messagebox.askyesno("完成", "为了执行您的操作,请点击确定重新启动程序!")
        if restart:
            os.execv(sys.executable, ['python'] + sys.argv)

    def exception(self, error):
        messagebox.showerror("神秘错误", f"发生了神秘错误! {error}")

    # 正常状态图片播放
    def set_pet_image(self):
        try:
            image = Image.open(self.pet_info_config['pet_info']['main_image_path'])
            image = image.resize((self.width, self.height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.pet_image = tk.Label(self, image=photo, bg=self.TRANSCOLOUR)
            self.pet_image.pack(expand=True, fill="both")
            self.pet_image.image = photo  # 保持引用

            # 确保图片加载完毕后再调用呼吸函数
            self.breathing_in_out()
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

    def breathing_in_out(self):
        try:
            new_width = int(self.width * (1 + self.breathing_factor))
            new_height = int(self.height * (1 + self.breathing_factor))
            
            image = Image.open(self.pet_info_config['pet_info']['main_image_path'])
            image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.pet_image.config(image=photo)
            self.pet_image.image = photo

            # 反向进行动画
            self.breathing_factor *= -1
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

        # 递归
        self.after(self.breathing_speed, self.breathing_in_out)


    # 动画播放函数
    def animation_player(self, action_name):
        action_config = self.pet_menu_config['menu_items'].get(action_name)

        self.move = action_config.get('move', False)
        self.end_until_sound = action_config.get('end_until_sound', False)
        self.multi_sound = action_config.get('multi_sound', False)

        self.simple_animation_play(action_config, False)

    def simple_animation_play(self, action_config, auto): 
        self.stop_animation_play()

        self.animation = TkGifWidget.AnimatedGif(master=self.pet_image, file_path=action_config.get('image_path'), play_mode="display", loop=None, bg=self.TRANSCOLOUR)
        self.animation.pack(expand=True, fill="both")
        
        if self.multi_sound:
            try:
                sound_path = random.choice(action_config.get('sound_path', []))
            except FileNotFoundError as e:
                self.file_not_found_error(e)
            except TypeError as e:
                self.type_error(e)
            except Exception as e:
                self.exception(e)
        else:
            try:
                sound_path = action_config.get('sound_path')
            except FileNotFoundError as e:
                self.file_not_found_error(e)
            except TypeError as e:
                self.type_error(e)
            except Exception as e:
                self.exception(e)
        
        if self.move:
            self.moving = True
            self.move_animation_play(action_config)

        try:
            winsound.PlaySound(sound_path, winsound.SND_ASYNC | winsound.SND_FILENAME)  #播放音频
        except RuntimeError as e:
            self.runtime_error(e)
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)
        
        if self.end_until_sound:
            self.animation.loop = 0
            sound_clip = AudioFileClip(sound_path)
            sound_time = sound_clip.duration
            self.animation.after(int(sound_time * 1000), func=self.stop_animation_play)
        else:
            self.animation.play_end_func = self.stop_animation_play

    def move_animation_play(self, action_config):
        if action_config.get('is_move_right'):
            if not self.moving:
                return
            try:
                step = action_config.get('move_speed')
            except FileNotFoundError as e:
                self.file_not_found_error(e)
            except TypeError as e:
                self.type_error(e)
            except Exception as e:
                self.exception(e)
            x = self.winfo_x()
            new_x = x + step
            self.geometry(f"+{new_x}+{self.winfo_y()}")
            self.after(100, lambda: self.move_animation_play(action_config))
        else:
            if not self.moving:
                return
            try:
                step = action_config.get('move_speed')
            except FileNotFoundError as e:
                self.file_not_found_error(e)
            except TypeError as e:
                self.type_error(e)
            except Exception as e:
                self.exception(e)
            x = self.winfo_x()
            new_x = x - step
            self.geometry(f"+{new_x}+{self.winfo_y()}")
            self.after(100, lambda: self.move_animation_play(action_config))

    def auto_animation_play(self):
        auto_actions = list(self.pet_menu_config['auto_items'].keys())
        auto_action = random.choice(auto_actions)
        action_config = self.pet_menu_config['auto_items'].get(auto_action)

        self.simple_animation_play(action_config, True)

    def stop_animation_play(self, *args):
        if self.animation:
            try:
                self.animation.destroy()
            except AttributeError as e:
                self.attribute_error(e)
        self.animation = None
        self.moving = False
        try:
            winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_FILENAME)  #播放音频
        except RuntimeError as e:
            self.runtime_error(e)
        except FileNotFoundError as e:
            self.file_not_found_error(e)
        except Exception as e:
            self.exception(e)

    # 角色切换函数
    def change_pets(self, pet_name):
        pets_path = "Pets"
        for pet_folder in os.listdir(pets_path):
            pet_folder_path = os.path.join(pets_path, pet_folder)
            config_folder_path = os.path.join(pet_folder_path, "Config")
            info_file_path = os.path.join(config_folder_path, "Info.json")
            
            if os.path.isfile(info_file_path):
                try:
                    with open(info_file_path, 'r', encoding='utf-8') as info_file:
                        info_data = json.load(info_file)

                        current_pet_name = info_data.get('pet_info', {}).get('name')
                        current_path_name = info_data.get('pet_info', {}).get('path_name')

                        if current_pet_name == pet_name:
                            # 更新 Config.json 中的 master 项
                            config_path = "Config\\Config.json"
                            with open(config_path, 'r', encoding="utf-8") as file:
                                config_data = json.load(file)
                            config_data['pets']['master'] = current_path_name
                            
                            with open(config_path, 'w', encoding="utf-8") as file:
                                json.dump(config_data, file, ensure_ascii=False, indent=4)
                            
                            # 重新加载宠物信息
                            self.load_pet_info_json(f"Pets\\{current_path_name}\\Config\\Info.json")
                            self.load_pet_menu_json(f"Pets\\{current_path_name}\\Config\\Menu.json")

                except json.JSONDecodeError as e:
                    self.json_decode_error(e)
                except FileNotFoundError as e:
                    self.file_not_found_error(e)
                except Exception as e:
                    self.exception(e)

    # 菜单绑定的其他函数与小托盘绑定的函数
    def create_settings_window(self):
        settings_window = SettingsWindow()
    
    def show_window(self):
        self.deiconify()
        self.icon.stop()
        
    def show_message(self):
        self.icon.notify("Warma", "啊——蜘蛛啊——")
        
    def quit_window(self):
        self.icon.stop()
        self.destroy()
    
    def unshow_window(self, image_path):
        self.withdraw()
        menu = (pystray.MenuItem(text="启动", action=self.show_window, default=True),
                pystray.MenuItem(text="啊——", action=self.show_message),
                pystray.MenuItem(text="退出", action=self.quit_window)
        )
        image = Image.open(image_path)
        self.icon = pystray.Icon("沃玛桌宠", image, "nia~", menu)
        self.icon.run()

    def exit_window(self):
        self.destroy()

    # 菜单函数
    def create_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        for menu_item_name in self.pet_menu_config['menu_items']:
            menu.add_command(label=menu_item_name, command=lambda name=menu_item_name: self.animation_player(name))
        menu.add_separator()

        for menu_item_pets_name in self.pet_names:
            menu.add_command(label=f"切换角色为{menu_item_pets_name}", command=lambda name=menu_item_pets_name: self.change_pets(name))
        menu.add_separator()
        # 添加其他菜单项
        menu.add_command(label="停止", command=self.stop_animation_play)
        menu.add_command(label="设置", command=self.create_settings_window)
        menu.add_separator()
        menu.add_command(label="收入小托盘", command=lambda: self.unshow_window("icon.ico"))
        menu.add_command(label="再见", command=self.exit_window)
        menu.post(event.x_root, event.y_root)

    # 事件绑定函数  
    def bind_mouse_menu(self):
        self.bind("<Button-3>", self.create_menu)

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