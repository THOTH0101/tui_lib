import os

from constant import LIB_PATH


def get_lib_content():
    if os.path.exists(LIB_PATH):
        content = os.listdir(LIB_PATH)
        return content
    os.mkdir(LIB_PATH)
