import os
import shutil

from constant import LIB_PATH
from functions.helper_functions import remove_lib_empty_dirs


def remove_ebook_recursive():
    contents = os.listdir(LIB_PATH)
    for content in contents:
        content_path = os.path.join(LIB_PATH, content)
        remove_ebook(content_path)
    return "Success: all ebook deleted"


def remove_ebook(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    if os.path.isfile(file_path):
        return "Error: invalid ebook record"

    shutil.rmtree(file_path)
    remove_lib_empty_dirs()
    return "Success: ebook deleted"
