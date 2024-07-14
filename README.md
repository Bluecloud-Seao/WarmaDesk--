# **<font class="text-color-7" color="#03a9f4">WarmaDesk-沃玛桌宠 1.2.0_240714</font>**
* ### 程序介绍
沃玛桌宠是一款桌面宠物软件，由刚小学毕业的B站用户“只是一个球_”独立开发5天，程序中形象来自于B站知名UP主“[Warma](https://space.bilibili.com/53456)”，灵感来源于B站UP主“[Funtime工作室](https://space.bilibili.com/629852514)”，向以上提到的两位UP主表示感谢！

目前程序版本：1.2.0_240714  
README.md版本：第一版第一次修订   
请更新时记得修改。  

我在B站上发布了[软件宣传片](https://space.bilibili.com/1858500718)，也许在宣传片中各位沃沃头都感觉很不错，但事实上这款软件真的全是BUG——尤其是设置窗口——因此体验大抵是很不佳的。但由于我一个人没有那么多的力气从事开发，所以只得如此草草发布第一版——即1.1.0_240708。但各位沃沃头们也不要失望，我一定会尽自己所能继续更新的——在不耽误学业和生活的情况下。

阅读我的源代码（main.py&settings.py）大家会发现这个程序只是一个GIF与音频播放器，非常简单，所以大家都可以对这个程序进行改编，也是在帮助我完善这个程序。如果有人这么做的话，我将会诚恳地说一声：“谢谢”

* ### TkGifWidget模块声明
这个模块由B站UP主[水母山楂](https://space.bilibili.com/375499948)制作，采用WTFPL开源协议，模块文件在libs目录下，并包含License和Readme。在最近，经过我意见的提出，作者更新了这个模块，添加了“play_end_func”，即播放结束后执行的函数，在此感谢作者采纳我的意见。但是因此软件是播放音频为主的，所以我目前先采用了moviepy模块提供的duration方式以检测音频的时长再用after函数计时——当然，等到之后的版本添加了自定义图片和音频功能后肯定是要用“play_end_func”这个方式的。最后，还是真诚地感谢作者！
* ### 使用方式
安装完成后程序会自动添加至开机自启动，即一开机桌面上就有沃玛（不需要可以自己禁用，右键任务栏点击任务管理器，然后点击“启动应用”禁用“WarmaDesk.exe"即可停止开机自启动）

看见Warma之后，鼠标左键长按Warma并拖动可移动Warma，右键可打开功能菜单——播放动画或执行其他操作。

选择菜单项“设置”之后，显示设置窗口，设置窗口标题栏为作者自行编写，因此操作方法与传统窗口不同。鼠标左键点击窗口标题可全屏窗口（含有标题变大的BUG），右键即可恢复大小。鼠标左键长按顶端蓝色区域并拖动可更改窗口位置（与传统窗口无异）。鼠标左键点击右上角“X”可关闭窗口，右键点击则缩小窗口。

选择菜单项“收入小托盘”（即免打扰模式）后，程序图标就是Warma，右键即可打开菜单。

* ### 软件中的图片
![](https://markdown.liuchengtu.com/work/uploads/upload_5492772fba214302bafb53db95729429.png)
![](https://markdown.liuchengtu.com/work/uploads/upload_9e4094420f36c537b528cfdd5bdf25db.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_1b8a198a203324a8f61a8ff45f545ae2.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_05e357c38686df5f4ed6ecfa9500d192.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_07b5db194be947637b25f4b615c70a3c.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_98cc11de8ebc30e96f70e088ae49a4a1.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_7a8efc7584f97b4d30cbd6155e7ce83a.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_919a25a38233479d10647b70e3849afa.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_fa7defe1ddb032f33413563dd00c6f75.gif)
![](https://markdown.liuchengtu.com/work/uploads/upload_4b59d4e54bac252bde922fb36c57dd31.gif)

最后，感谢您支持我，谢谢！

1.1.0_240708第一版：2024年7月10日
1.2.0_240714第一版第一次修订：2024年7月14日

