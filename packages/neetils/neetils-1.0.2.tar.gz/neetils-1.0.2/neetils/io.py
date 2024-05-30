"""
@File    :   io.py
@Time    :   2024/04/25 09:55:59
@Author  :   TankNee
@Version :   1.0
@Desc    :   IO Tools
"""


import json
from tqdm import tqdm
import yaml

def read_jsonl(file_path):
    with open(file_path, 'r') as f:
        basename = file_path.split('/')[-1]
        data = f.readlines()
        results = []
        for line in tqdm(data, desc=basename, leave=False):
            results.append(json.loads(line))
    return results

def write_jsonl(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        for line in data:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def write_yaml(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)