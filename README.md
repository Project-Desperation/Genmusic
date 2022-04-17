# Genmusic
将midi文件转换为键盘按键序列，并自动弹奏，依赖pykeyboard等第三方库，详见 **requirements.txt**

## MIDI解析

**midi.py** 将mid文件转换为txt乐谱：

```shell
python midi.py --input=path/to/midi --output=path/to/txt
```

## 自动弹奏

自动弹奏脚本 **main.exe**，来自[用python实现原神弹琴脚本~胡桃摇](https://www.bilibili.com/video/BV1pY41137QH)

**music** 文件夹存储乐谱文件，乐谱中+代表一拍，-代表半拍，=代表四分之一拍，第一行输入每拍间隔，已设置好了