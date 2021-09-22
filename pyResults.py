#!/usr/bin/env python3

from io import BufferedReader
from os import path
import sys
import argparse
import pathlib
import logging
import re


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_file_type(file_path: pathlib.Path):
    if not file_path.is_file():
        logger.error(f'cannot open file {file_path}')
        exit()

    f = file_path.open(mode='r', encoding='utf8')
    head = f.readline().rstrip()
    f.close()
    if head == '#!MLF!#':
        return 'mlf'
    elif re.match(r'\S+\s.*', head):
        return 'txt'
    else:
        return None


def load_txt_file(file_path: pathlib.Path):
    if not file_path.is_file():
        logger.error(f'cannot open file {file_path}')
        exit()
    
    f = file_path.open(mode='r', encoding='utf8')
    d = {}
    for line in f:
        try:
            name, trans = line.rstrip().split(' ', 1)
        except ValueError:
            logger.error(f'{file_path}格式错误，请检查文件空格')
            exit()
        trans = list(trans)
        trans = [c.strip() for c in trans if c.strip() != '']
        if name in d:
            logger.error(f'{name} is duplicated')
            exit()
        d[name] = trans
    f.close()
    return d


def load_mlf_file(file_path: pathlib.Path):
    if not file_path.is_file():
        logger.error(f'cannot open file {file_path}')
        exit()
    
    f = file_path.open(mode='r', encoding='utf8')
    d = {}
    _ = f.readline()
    for line in f:
        m = re.match(r'"\*\/(\S+)\.[labrec]{3}"', line.rstrip())
        if m:
            name = m.group(1)
            d[name] = []
            while True:
                c = f.readline().rstrip()
                if c == '.': break
                d[name].append(c)
        else:
            logger.error(f'{file_path}格式错误，请确保是mlf文件')
            exit()

    f.close()
    return d



def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.

    Main algorithm used is dynamic programming.

    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''

    d = [ [ 0 for _ in range(len(h) + 1 )] for _ in range(len(r) + 1)]
    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d


def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.

    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0: 
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]


def alignedPrint(list, r, h):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
    '''
    print("REF:", end=" ")
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(" "*(len(h[index])), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print(r[index1] + " " * (len(h[index2])-len(r[index1])), end=" ")
            else:
                print(r[index1], end=" "),
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(r[index], end=" "),
    print("\nHYP:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print(h[index2] + " " * (len(r[index1])-len(h[index2])), end=" ")
            else:
                print(h[index2], end=" ")
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(h[index], end=" ")
    print("\nEVA:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(r[index])-1), end=" ")
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(h[index])-1), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print("S" + " " * (len(r[index1])-1), end=" ")
            else:
                print("S" + " " * (len(h[index2])-1), end=" ")
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
    print("")


def wer(d_ref, d_hyp, is_align=False, is_full=False):
    """
    This is a function that calculate the word error rate in ASR.
    """

    total_count = 0
    total_sub = 0
    total_ins = 0
    total_del = 0

    for i, name in enumerate(d_hyp):
        if not name in d_ref:
            logger.error(f'cannot find {name} in {ref}')
            exit()
        
        # build the matrix
        ed = editDistance(d_ref[name], d_hyp[name])

        # find out the manipulation steps
        step_list = getStepList(d_ref[name], d_hyp[name], ed)

        n = len(d_ref[name])
        n_cor = step_list.count('e')
        n_ins = step_list.count('i')
        n_sub = step_list.count('s')
        n_del = step_list.count('d')

        if is_full:
            # print every result
            print(f'SEN: {name}')
            wer = float(ed[len(d_ref[name])][len(d_hyp[name])]) / len(d_ref[name]) * 100
            corr = 100 - (n_sub + n_del) / n * 100
            acc = 100 - wer
            e_ins = n_ins / n * 100
            e_sub = n_sub / n * 100
            e_del = n_del / n * 100

            if is_align:
                # print the result in aligned way
                alignedPrint(step_list, d_ref[name], d_hyp[name])

            print(f"%Corr={corr:.2f}, Acc={acc:.2f}, WER: {wer:.2f}(Sub={e_sub:.2f}, Del={e_del:.2f}, Ins={e_ins:.2f})")

        total_count += n
        total_ins += n_ins
        total_sub += n_sub
        total_del += n_del

    e_ins = total_ins / total_count * 100
    e_sub = total_sub / total_count * 100
    e_del = total_del / total_count * 100
    wer = (total_ins + total_sub + total_del ) / total_count * 100
    corr = 100 - (total_sub + total_del ) / total_count * 100
    acc = 100 - wer
    print("---------- Overall Results ----------")
    print(f"%Corr={corr:.2f}, Acc={acc:.2f}, WER: {wer:.2f}(Sub={e_sub:.2f}, Del={e_del:.2f}, Ins={e_ins:.2f})")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='字错（CER）计算工具python版。问题反馈请联系xu.li@aispeech.com')
    parser.add_argument('ref', type=pathlib.Path, help='人工标注文件路径')
    parser.add_argument('hyp', type=pathlib.Path, help='识别结果文件路径')

    parser.add_argument('-f', action="store_true", help='逐句显示统计结果')
    parser.add_argument('-t', action="store_true", help='逐句对齐展示文本')
 
    args =parser.parse_args()
    
    ref = args.ref
    hyp = args.hyp
    is_align = args.t
    is_full = args.t or args.f 

    file_type = get_file_type(ref)

    if file_type == 'txt':
        d_ref = load_txt_file(ref)
        d_hyp = load_txt_file(hyp)
    elif file_type == 'mlf':
        d_ref = load_mlf_file(ref)
        d_hyp = load_mlf_file(hyp)
    else:
        logger.error(f'非法文件格式')
        exit()

    wer(d_ref, d_hyp, is_align, is_full)
