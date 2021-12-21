#!/usr/bin/env python3
"""
录音文件转写识别日志转txt.
"""
import json
import os
import re
import argparse


parser = argparse.ArgumentParser(usage="python3 read_json_for_task.py json_dir >out.txt",
                                 description="Json识别日志转txt.")
parser.add_argument("json_dir", type=str, help='Json日志目录')
args = parser.parse_args()

json_dir = os.path.abspath(args.json_dir)
json_list = [name for name in os.listdir(json_dir) if name.endswith('.json')]
for json_file in json_list:
    json_file = os.path.join(json_dir,json_file)
    id_ = os.path.splitext(os.path.basename(json_file))[0]
    id_ = id_.split('.')[0]
    with open(json_file, 'r', encoding='utf8') as j:
        data = json.load(j)
        print(id_, end=' ')
        if data.get('data', 0):
            result = data['data']['result']
        elif data.get('result', 0):
            result = data['result']
        else:
            print("不支持的日志格式")
            exit()
        for res in result:
            onebest = re.sub(r'[，。？！、]',"",res["onebest"])
            print(onebest, end="")
        print('')
