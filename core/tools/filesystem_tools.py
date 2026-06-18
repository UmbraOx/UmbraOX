# core/tools/filesystem_tools.py

import os


def create_file(path, content=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return True


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    return True