# Genmusic
将midi文件转换为键盘按键序列，并自动弹奏，依赖pykeyboard等第三方库，详见 **requirements.txt**

## MIDI解析

**midi.py** 将mid文件转换为txt乐谱：

```shell
python midi.py --input=path/to/midi --output=path/to/txt
```

## 自动弹奏

自动弹奏脚本 **main.exe**，来自[**MRevenger**](https://space.bilibili.com/59428319)的[用python实现原神弹琴脚本~胡桃摇](https://www.bilibili.com/video/BV1pY41137QH)，以下为搬运的使用说明

使用时记得用管理员模式运行原神弹琴.exe main.exe和music放在同级文件夹里，不要把main.exe移动到其它位置，否则无法识别 更新后可以使用中文名作为乐谱文件名名字长度最好别超过12个字(●ˇ∀ˇ●)

**music** 文件夹存储乐谱文件，乐谱中+代表一拍，-代表半拍，=代表四分之一拍，第一行输入每拍间隔，已设置好了。