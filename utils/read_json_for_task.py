#!/usr/bin/env python3

import json
import sys
import os
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("json_dir", type=str, help='识别结果目录')
args = parser.parse_args()
json_dir = os.path.abspath(args.json_dir)
json_list = [name for name in os.listdir(json_dir) if name.endswith('.json')]
for json_file in json_list:
    json_file = os.path.join(json_dir,json_file)
    id_ = os.path.splitext(os.path.basename(json_file))[0]
    id_ = id_.split('.')[0]
    with open(json_file, 'r') as j:
        data = json.load(j)
        print(id_, end=' ')
        for res in data['result']:
            onebest = re.sub(r'[，。？！、]',"",res["onebest"])
            print(onebest, end="")
        print('')
        
