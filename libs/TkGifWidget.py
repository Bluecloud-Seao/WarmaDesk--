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
            file_path=None,
            play_mode: Literal['click', 'display', 'hover'] = CLICK,
            default_bg=None,
            bg_func=None,
            nogif_bg=None,
            hover_func=None,
            play_end_func=None,
            loop=-1,
            master=None,
            **kwargs
    ):
        """
        Args:
            file_path: GIF动图文件路径。值为None（默认值）代表在创建控件后指定动图，指定的方式是使用set_gif()方法
            play_mode: 播放模式，有以下三种，默认值为“click”：
                1)click：点击前显示背景图，点击后播放动图，再次点击重新显示背景图。
                2)display：动图控件被映射时开始播放动图，取消映射时结束播放动图。
                3)hover：当鼠标移动到动图控件上时播放动图，移出动图控件结束播放动图。
            default_bg: 默认背景图，值为路径或Image对象。在没播放动图时显示的图片，默认使用动图的第一张图片。
            bg_func: 值为处理背景图的函数（或方法），调用时会传入背景图的Image对象，返回值应是一个Image对象。
                     如果值为None（默认）则不处理背景图。
                     值也可以为一个包含上述函数（或方法）的序列，背景图的Image对象会依次被该序列的每个函数（或方法）处理。
            nogif_bg：没有指定动图时使用的背景图，值为路径或Image对象。若同时指定default_bg和nogif_bg，在没有指定动图时
                      使用nogif_bg，在指定动图时使用default_bg。
            hover_func: 播放模式是hover时点击控件执行的函数，AnimatedGif控件作为位置参数传入此函数。
                        值为None（默认）时或播放模式不是hover时无效果。
            loop: GIF循环次数。值为0代表无限循环，值为None代表不循环，-1（默认）采取GIF动图的设置。
                  总播放次数=1+loop
            play_end_func：动图播放结束时执行的函数，AnimatedGif控件、是否还会继续循环播放（布尔型）作为位置参数传入此函数。
                           值为None（默认）时无效果。
            master: 父控件。
            **kwargs: 传入Frame控件的关键字参数。
        """
        super().__init__(master, **kwargs)

        self.__first_img = None
        self.__bg_img = None
        self.__bg_imgtk = ''
        self.__play_mode = play_mode
        self._cbid = None

        self.play_state: Literal['run', 'stop'] = 'stop'  # 指示当前播放状态
        self.loop = loop  # GIF循环次数
        self.remain_loop: int = -1  # 剩余的循环播放次数，-1表示无限循环播放
        self.image_lst = []  # 每帧图像组成的列表
        self.duration_lst = []  # 每帧图像对应的持续时间组成的列表
        self.image_iter = iter([])  # 图像序列的迭代器
        self.duration_iter = iter([])  # 持续显示时间序列的迭代器
        self.play_end_func = play_end_func  # 动图播放结束时执行的函数
        self.hover_func = hover_func  # 播放模式是hover时点击控件执行的函数
        self.bg_func = bg_func  # 处理背景图的函数（或方法）。当背景图修改时会自动应用
        self.default_bg = default_bg  # 默认背景图
        self.nogif_bg = nogif_bg  # 无动图时背景图

        # 创建动图的容器
        self.img_container = tk.Label(self, image=self.bg_imgtk, bd=0)
        self.img_container.pack(fill='both', expand=True)

        if file_path:
            self.set_gif(file_path)
        elif nogif_bg:
            self.set_bg_img(nogif_bg)
        elif default_bg:
            self.set_bg_img(default_bg)

    def set_play_mode(self, play_mode: Literal['click', 'display', 'hover']):
        """设置当前播放模式"""
        if play_mode not in ['click', 'display', 'hover']:
            raise ValueError('The value of the play_mode should be one of the click, display or hover.')
        self.__play_mode = play_mode
        # 重置光标，解除事件绑定
        self.img_container.config(cursor='')
        if not hasattr(self.img_container, '_bind_lst'):
            self.img_container._bind_lst = []
        for i, j in self.img_container._bind_lst:
            self.img_container.unbind(i, j)

        self.img_container._bind_lst = bind_lst = []  # 将绑定的事件添加到内部列表，方便解除绑定
        # 若当前未指定动图，则不进行事件绑定
        if self.image_lst:
            if play_mode == 'click':
                bind_lst.append(
                    ('<Button-1>', self.img_container.bind('<Button-1>', func=lambda x: self._click_to_switch()))
                )
                self.img_container.config(cursor='hand2')
            elif play_mode == 'display':
                bind_lst.extend(
                    [
                        ('<Map>', self.img_container.bind('<Map>', func=lambda x: self.start_play(), add=True)),
                        ('<Unmap>', self.img_container.bind('<Unmap>', func=lambda x: self.end_play(), add=True))
                    ]
                )
                # 如果当前动图控件正在映射，则直接开始播放
                if self.play_state == 'stop' and self.img_container.winfo_ismapped():
                    self.start_play()
            elif play_mode == 'hover':
                bind_lst.extend(
                    [
                        ('<Enter>', self.img_container.bind('<Enter>', func=lambda x: self.start_play(), add=True)),
                        ('<Leave>', self.img_container.bind('<Leave>', func=lambda x: self.end_play(), add=True))
                    ]
                )
                if self.hover_func is not None:
                    self.img_container.config(cursor='hand2')
                    bind_lst.append(
                        (
                            '<Button-1>',
                            self.img_container.bind('<Button-1>', func=lambda x: self.hover_func(self), add=True))
                    )
                # 如果当前鼠标正在动图控件上，则直接开始播放，否则结束播放
                try:
                    if (pos := self.img_container.winfo_pointerxy()) != -1 and \
                            self.winfo_containing(*pos) is self.img_container:
                        if self.play_state == 'stop':
                            self.start_play()
                    else:
                        self.end_play()
                except KeyError:  # 若pos位置是控件的某些部分winfo_containing()会抛出KeyError
                    self.end_play()

    def set_gif(self, file_path):
        """根据文件路径file_path设置控件的GIF动图。如果file_path为None，则将当前动图指定为空"""
        # 暂停当前动图播放
        self.end_play()
        if file_path:
            # 根据file_path打开图像文件，创建其图像及其对应持续显示时间的序列
            with Image.open(file_path) as im:
                sequence = ImageSequence.Iterator(im)
                self.image_lst = []
                self.duration_lst = []
                for i in sequence:
                    self.image_lst.append(ImageTk.PhotoImage(i))
                    self.duration_lst.append(i.info["duration"])
                im.seek(0)
                # 设置背景图
                self.__first_img = im.copy().convert('RGBA')
                self.set_bg_img(self.default_bg)
                # 根据loop设置循环次数
                loop = self.loop
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
        else:
            self.image_lst = []
            self.duration_lst = []
            self.__first_img = None
            if self.nogif_bg:
                self.set_bg_img(self.nogif_bg)
            else:
                self.set_bg_img(self.default_bg)

        self.set_play_mode(self.play_mode)

    @property
    def bg_img(self):
        return self.__bg_img

    @bg_img.setter
    def bg_img(self, _):
        raise Exception('Please use set_bg_img() method to set the background image.')

    @property
    def bg_imgtk(self):
        return self.__bg_imgtk

    @property
    def play_mode(self):
        return self.__play_mode

    @play_mode.setter
    def play_mode(self, _):
        raise Exception('Please use set_play_mode() method to set the play mode.')

    def set_bg_img(self, value):
        """
        根据value设置背景图，然后进行后续处理。若value为None，则将背景图设置为动图的第一张图片（若有）；若
        为Image对象，则直接设置；否则，视为背景图路径。
        注意此方法是设置当前的背景图，若想设置默认背景图，请修改default_bg属性
        """
        if not value:
            if self.__first_img:
                self.__bg_img = self.__first_img
            else:
                self.__bg_img = None
        elif isinstance(value, Image.Image):
            self.__bg_img = value
        else:
            self.__bg_img = Image.open(value)

        if self.__bg_img:
            self.apply_bg_func()

    def apply_bg_func(self, bg_func=None):
        """将处理背景图的函数bg_func或该函数对象组成的序列应用到背景图的Image对象上"""
        if not bg_func:  # 当bg_func为None时采用实例属性
            bg_func = self.bg_func
        if bg_func:  # 当bg_func为None且实例属性bg_func也为None时，跳过应用bg_func
            if isinstance(bg_func, Sequence):
                for func in bg_func:
                    self.__bg_img = func(self.__bg_img)
            else:
                self.__bg_img = bg_func(self.__bg_img)

        self._update_bg_img()

    def _update_bg_img(self):
        """更新控件的背景图"""
        self.__bg_imgtk = ImageTk.PhotoImage(self.__bg_img)
        if self.play_state == 'stop':
            self.img_container.configure(image=self.bg_imgtk)

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
        if self._cbid is not None:
            self.after_cancel(self._cbid)
        self.img_container.configure(image=self.bg_imgtk)  # 恢复背景图

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
                if self.play_end_func:
                    self.play_end_func(self, False)
                return
            elif self.remain_loop != -1:
                self.remain_loop -= 1
            self._update_iter()
            if self.play_end_func:
                self.play_end_func(self, True)
        else:
            self.img_container.configure(image=img)
        # 记录延迟回调的id，便于取消
        self._cbid = self.after(
            duration, self._next_frame
        )


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
