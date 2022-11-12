# 手动JSON数据库操作集合
import json
import os


def find_database(database_name: str) -> bool:
    for filename in os.listdir():
        if filename == database_name:
            return True
    return False


def read_database(database_name: str) -> str:
    if find_database(database_name):
        with open(database_name, "r", encoding="utf-8") as f:
            info = f.read()
    else:
        info = "N/A"
    return info


def parse_database(database_name: str) -> dict:
    info = read_database(database_name)
    if info == "N/A":
        return {'data': []}
    else:
        try:
            information = json.loads(info)
        except json.JSONDecodeError:
            return {'data': []}
        else:
            return eval(str(information))


def write_database(database_name: str, info: dict) -> bool:
    with open(database_name, "w", encoding="utf-8") as f:
        information = json.dumps(info, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ':'))
        f.write(information)
    return True
