import mimetypes
import os
from pathlib import Path

from constant import LIB_PATH


def remove_empty_dir(file_path):
    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)
        path = Path(content_path)

        # return if directory is not empty
        if any(path.iterdir()):
            return
        path.rmdir()
    path = Path(file_path)
    path.rmdir()


def remove_lib_empty_dirs():
    contents = os.listdir(LIB_PATH)
    for content in contents:
        content_path = os.path.join(LIB_PATH, content)
        remove_empty_dir(content_path)


def is_ebook_extension(file_path):
    SUPPORTED_EXTENSIONS = {".epub", ".pdf", ".mobi", ".azw3", ".fb2"}

    return Path(file_path).suffix.lower() in SUPPORTED_EXTENSIONS


def is_valid_ebook(file_path):
    path = Path(file_path)
    if not is_ebook_extension(path):
        return False

    mime_type, _ = mimetypes.guess_type(path)

    EBOOK_MIMES = [
        "application/epub+zip",
        "application/pdf",
        "application/x-mobipocket-ebook",
        "application/vnd.amazon.mobi8-kindle-archive",
    ]

    return mime_type in EBOOK_MIMES
