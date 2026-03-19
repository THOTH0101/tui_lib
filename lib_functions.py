import os
import shutil
import mimetypes
import epub_meta

from enum import Enum
from pathlib import Path
from constant import LIB_PATH
from pypdf import PdfReader


class EbookTypes(Enum):
    EPUB = "application/epub+zip"
    PDF = "application/pdf"


def get_lib_content():
    if os.path.exists(LIB_PATH):
        content = os.listdir(LIB_PATH)
        return content
    os.mkdir(LIB_PATH)


def add_ebook_recursive(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    if os.path.isfile(file_path):
        return add_ebook(file_path)

    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)

        if os.path.isfile(content_path):
            if is_valid_ebook(content_path):
                print(add_ebook(content_path))
            continue
        else:
            new_path = os.path.join(file_path, content)
            print(f"Directory: {new_path}")
            add_ebook_recursive(new_path)


def add_ebook(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    mime_type, _ = mimetypes.guess_type(file_path)

    # add ebook base to library
    if mime_type == EbookTypes.EPUB.value:
        meta_data = epub_meta.get_epub_metadata(file_path)
        authors = ",".join(meta_data["authors"]) or "Unknown"
        title = meta_data["title"].replace("/", " ") or "Unknown"
        dest_path = f"{LIB_PATH}/{authors}/{title}/{title} - {authors}.epub"

        print(f"Copying ebook file from {file_path} to {dest_path}")
        dir_name = os.path.dirname(dest_path)
        if dir_name != "" and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        shutil.copy2(file_path, dest_path)
        return f"Success: {file_path} added"

    if mime_type == EbookTypes.PDF.value:
        meta_data = PdfReader(file_path).metadata
        authors = meta_data.author or "Unknown"
        title = meta_data.title.replace("/", " ") or "Unknown"
        dest_path = f"{LIB_PATH}/{authors}/{title}/{title} - {authors}.pdf"

        print(f"Copying ebook file from {file_path} to {dest_path}")
        dir_name = os.path.dirname(dest_path)
        if dir_name != "" and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        shutil.copy2(file_path, dest_path)
        return f"Success: {file_path} added"

    return "Error: invalid ebook type"


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
