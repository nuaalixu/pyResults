#!/bin/env python3

import sys

def is_english_char(ch):
    if '\u0041' <= ch <= '\u005a' or '\u0061'<= ch <='\u007a' or ch =="'":
        return True
    return False


def is_chinese_char(ch):
    if '\u4e00' <= ch <= '\u9fa5':
        return True
    return False

def convert(f):
    print('#!MLF!#')
    for l in f:
        mlist = l.strip('\n').split()
        mlist = list(filter(lambda x : x, mlist))
        text = ' '.join(mlist[1:])
        print(f'"*/{mlist[0]}.lab"')
        en_word=''
        if len(text) == 0:
            print('NULL')
        else:
            for c in text:
                if is_english_char(c):
                    en_word = en_word + c
                    continue
                if is_chinese_char(c):
                    if len(en_word)>0:
                        print(en_word)
                        en_word=''
                    print(c)
            if len(en_word) > 0: print(en_word)
        print('.')


if len(sys.argv) > 1 :
    file_path = sys.argv[1]
    f = open(file_path,'r',encoding='utf-8')
    convert(f)
    f.close()
elif not sys.stdin.isatty():
    f = sys.stdin
    convert(f)
else:
    print("Usage: script.py [fileaname|stdin]")
    print("Convert kaldi text file to htk mlf file.")
