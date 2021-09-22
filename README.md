# pyResult
A tool for calculation CER (Character Error Rate) in Python.

## 使用方法

查看帮助信息:
```python
python3 pyResults -h
```

基础CER结果：
```
python3 pyResults ref.txt hyp.txt
```

详细信息:
```
python3 pyResults ref.txt hyp.txt
```

## 要求输入文本格式
支持kaldi的text文件和htk的mlf文件。

text文件格式:
```txt
标注文件
<id-1> <标注文本1>
<id-2> <标注文本2>
识别文件
<id-1> <识别文本1>
<id-2> <识别文本2>
```

mlf文件格式：
```
标注文件
#!MLF!#
"*/id-1.lab"
A
B
C
.
识别文件
#!MLF!#
"*/id-1.rec"
A
D
.
```

## 辅助工具
utils目录下是辅助脚本，主要用于文本文件的格式转换。
read_json_for_task.py，将录音文件转写的识别结果json文件转成标准txt文件。
label2txt.sh，将原始标注文本文件转成标准txt文件。
txt2mlf.py，将标准txt文件转mlf文件。
