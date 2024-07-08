"""一个用于显示GIF动图的Tk控件"""
import tkinter as tk
from typing import Literal, Sequence
from PIL import Image, ImageSequence, ImageTk, ImageDraw, ImageFilter, ImageEnhance

__all__ = ['AnimatedGif', 'CLICK', 'DISPLAY', 'HOVER', 'BgFunc']
CLICK = 'click'
DISPLAY = 'display'
HOVER = 'hover'


class AnimatedGif(tk.Frame):
    def __init__(
            self,
            file_path,
            play_mode: Literal['click', 'display', 'hover'],
            bg_path=None,
            bg_func=None,
            hover_func=None,
            loop=-1,
            master=None,
            **kwargs
    ):
        """
        Args:
            file_path: GIF动图文件路径。
            play_mode: 播放模式，有以下三种：
                1)click：点击前显示背景图，点击后播放动图，再次点击重新显示背景图。
                2)display：动图控件被映射时开始播放动图，取消映射时结束播放动图。
                3)hover：当鼠标移动到动图控件上时播放动图，移出动图控件结束播放动图。
            bg_path: 背景图路径。在没播放动图时显示的图片，默认使用动图的第一张图片。
            bg_func: 值为处理背景图的函数（或方法），调用时会传入背景图的Image对象，返回值应是一个Image对象。
                     如果值为None（默认）则不处理背景图。
                     值也可以为一个包含上述函数（或方法）的序列，背景图的Image对象会依次被该序列的每个函数（或方法）处理。
            hover_func: 播放模式是hover时点击控件执行的函数，AnimatedGif控件作为位置参数传入此函数。
                        值为None（默认）时或播放模式不是hover时无效果。
            loop: GIF循环次数。值为0代表无限循环，值为None代表不循环，-1（默认）采取GIF动图的设置。
            master: 父控件。
            **kwargs: 传入Frame控件的关键字参数。
        """
        super().__init__(master, **kwargs)

        # 根据file_path打开图像文件，创建其图像及其对应持续显示时间的序列
        with Image.open(file_path) as im:
            sequence = ImageSequence.Iterator(im)
            self.image_lst = []
            self.duration_lst = []
            for i in sequence:
                self.image_lst.append(ImageTk.PhotoImage(i))
                self.duration_lst.append(i.info["duration"])
            im.seek(0)
            self.first_img = im.copy().convert('RGBA')
            # 根据loop设置循环次数
            if loop is None or isinstance(loop, int) and loop >= -1:
                if loop == -1:
                    try:
                        self.loop = im.info['loop']
                    except KeyError:
                        self.loop = None
                else:
                    self.loop = loop
            else:
                raise ValueError('The value of the loop is wrong.')

        # 导入背景图
        if bg_path:
            self.bg_img = Image.open(bg_path)
        else:
            self.bg_img = self.first_img

        if bg_func:
            if isinstance(bg_func, Sequence):
                for func in bg_func:
                    self.bg_img = func(self.bg_img)
            else:
                self.bg_img = bg_func(self.bg_img)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # 创建动图的容器
        self.img_container = tk.Label(self, image=self.bg_img)
        self.img_container.pack(fill='both', expand=True)

        # 设置实例属性
        self.play_state: Literal['run', 'stop'] = 'stop'  # 指示当前播放状态
        self.remain_loop: int = -1  # 剩余的循环播放次数，-1表示无限循环播放
        self.image_iter = iter([])  # 图像序列的迭代器
        self.duration_iter = iter([])  # 持续显示时间序列的迭代器

        # 根据播放模式设置对应行为
        if play_mode not in ['click', 'display', 'hover']:
            raise ValueError('The value of the play_mode should be one of the click, display or hover.')
        if play_mode == 'click':
            self.img_container.bind('<Button-1>', func=lambda x: self._click_to_switch())
            self.img_container.config(cursor='hand2')
        elif play_mode == 'display':
            self.img_container.bind('<Map>', func=lambda x: self.start_play())
            self.img_container.bind('<Unmap>', func=lambda x: self.end_play(), add=True)
        elif play_mode == 'hover':
            self.img_container.bind('<Enter>', func=lambda x: self.start_play())
            self.img_container.bind('<Leave>', func=lambda x: self.end_play(), add=True)
            if hover_func is not None:
                self.img_container.config(cursor='hand2')
                self.img_container.bind('<Button-1>', func=lambda x: hover_func(self))

    def _click_to_switch(self):
        """播放模式为click的方法。根据播放状态对应开始或结束播放"""
        if self.play_state == 'run':
            self.end_play()
        elif self.play_state == 'stop':
            self.start_play()

    def start_play(self):
        """开始播放GIF动图"""
        if self.play_state == 'run':  # 若播放时调用此方法则重新播放
            self.end_play()

        self.play_state = 'run'
        # 设置剩余循环播放次数
        if self.loop is None:
            self.remain_loop = 0
        elif self.loop == 0:
            self.remain_loop = -1
        else:
            self.remain_loop = self.loop
        self._update_iter()
        self._next_frame()

    def end_play(self):
        """结束播放GIF动图"""
        self.play_state = 'stop'
        self.img_container.configure(image=self.bg_img)  # 恢复背景图

    def _update_iter(self):
        """根据图像序列和持续显示时间序列刷新对应迭代器"""
        self.image_iter = iter(self.image_lst)
        self.duration_iter = iter(self.duration_lst)

    def _next_frame(self):
        """按给定持续时间播放下一帧"""
        # 当play_state为stop时中暂停
        if self.play_state == 'stop':
            return
        img, duration = next(self.image_iter, -1), next(self.duration_iter, -1)
        # 判断是否结束此次播放
        if img == -1 or duration == -1:
            if self.remain_loop == 0:
                self.end_play()
                return
            elif self.remain_loop != -1:
                self.remain_loop -= 1
            self._update_iter()
        else:
            self.img_container.configure(image=img)
        self.after(duration, self._next_frame)


class BgFunc:

    @staticmethod
    def darken(img: Image.Image) -> Image.Image:
        """将图像变暗"""
        return ImageEnhance.Brightness(img).enhance(0.7)

    @staticmethod
    def gif_sign(img: Image.Image) -> Image.Image:
        """在图像中间添加灰色半透明圆圈附带添加GIF文本"""
        center = (img.size[0] // 2, img.size[1] // 2)  # 圆心
        # 圆的半径为图像宽高中的最小值的1/8取整
        r = min(img.size) // 8
        x = (center[0] - r, center[1] - r)
        y = (center[0] + r, center[1] + r)
        circle_img = Image.new('RGBA', size=img.size, color='#00000000')
        draw = ImageDraw.Draw(circle_img)
        draw.ellipse([x, y], fill='#8A8A8Bdd')
        draw.text(text='GIF', fill='white', xy=center, anchor='mm', font_size=r / 1.5)
        img = Image.alpha_composite(img, circle_img)
        return img

    @staticmethod
    def blur(img: Image.Image) -> Image.Image:
        """将图像模糊"""
        return img.filter(ImageFilter.GaussianBlur(1.5))
