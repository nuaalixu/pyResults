# pyResult
A tool for calculation WER (Word Error Rate) in Python.

## 使用方法

### 查看帮助信息
```python
python3 pyResults.py -h
```

### 统计信息总览
```
python3 pyResults.py data/ref.txt data/hyp.txt
```
预期结果
```
------------------------- Overall Results -------------------------
%Corr=87.50, Acc=84.29, WER: 15.71 [Sub=11.07, Del=1.43, Ins=3.21]
```

### 查看每句结果
```
python3 pyResults.py -f data/ref.txt data/hyp.txt
```
预期结果
```
C02E211102064_V1-3-4_202105040915_AD_NEAR-045: % 78.57 (57.14) [Sub=21.43, Del=0.00, Ins=21.43]
C02E211102064_V1-3-4_202105040915_AD_NEAR-046: % 100.00 (93.33) [Sub=0.00, Del=0.00, Ins=6.67]
C02E211102064_V1-3-4_202105040915_AD_NEAR-047: % 80.00 (80.00) [Sub=20.00, Del=0.00, Ins=0.00]
C02E211102064_V1-3-4_202105040915_AD_NEAR-049: % 100.00 (100.00) [Sub=0.00, Del=0.00, Ins=0.00]
------------------------- Overall Results -------------------------
%Corr=87.50, Acc=84.29, WER: 15.71 [Sub=11.07, Del=1.43, Ins=3.21]
```
Corr是正确率，Acc是准确率，WER是词错率（中文是字错率），Sub、Del和Ins分别表示插入错误、删除错误和插入错误。

### 每句对齐显示
```
python3 pyResults.py -t data/ref.txt data/hyp.txt
```
预期结果
```
Aligned transcription: C02E211102064_V1-3-4_202105040915_AD_NEAR-004
REF: 中 配 差 多 少 钱 呢 
HYP: 违 背 差 多   车 嘞 
EVA: S S     D S S 
------------------------- Overall Results -------------------------
%Corr=87.50, Acc=84.29, WER: 15.71 [Sub=11.07, Del=1.43, Ins=3.21]
```

## 输入文本格式
支持kaldi的text文件和htk的mlf文件。

### text格式
标注文件
```
<id-1> <标注文本1>
<id-2> <标注文本2>
```
识别文件
```
<id-1> <识别文本1>
<id-2> <识别文本2>
```

### mlf文件格式
标注文件
```
#!MLF!#
"*/id-1.lab"
A
B
C
.
```
识别文件
```
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
