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

text文件格式：
标注文件
```txt
<id-1> <标注文本1>
<id-2> <标注文本2>
```
识别文件
```txt
<id-1> <识别文本1>
<id-2> <识别文本2>
```