import os
import shutil
import mimetypes
import epub_meta

from enum import Enum
from datetime import datetime
from pathlib import Path
from constant import LIB_PATH
from pypdf import PdfReader


class EbookTypes(Enum):
    EPUB = "application/epub+zip"
    PDF = "application/pdf"


def get_books(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        return

    book_list = []
    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)
        if os.path.isfile(content_path):
            if not is_valid_ebook(content_path):
                continue
            book_list.append(get_book_info(content_path))
        else:
            print(f"Directory: {content_path}")
            new_list = get_books(content_path)
            if new_list:
                book_list.extend(new_list)
    return book_list


def remove_empty_dir(file_path):
    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)
        path = Path(content_path)
        if any(path.iterdir()):
            print(f"Error: {file_path} is not empty")
            return
        path.rmdir()
    path = Path(file_path)
    path.rmdir()


def clear_lib_dir():
    contents = os.listdir(LIB_PATH)
    for content in contents:
        content_path = os.path.join(LIB_PATH, content)
        remove_empty_dir(content_path)


def remove_ebook_recursive():
    contents = os.listdir(LIB_PATH)
    for content in contents:
        content_path = os.path.join(LIB_PATH, content)
        remove_ebook(content_path)


def remove_ebook(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist")
        return

    if os.path.isfile(file_path):
        print("Error: invalid ebook record")
        return

    shutil.rmtree(file_path)
    clear_lib_dir()
    print("Success: ebook deleted")


def add_ebook_recursive(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    if os.path.isfile(file_path):
        return add_ebook(file_path)

    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)

        if os.path.isfile(content_path):
            if not is_valid_ebook(content_path):
                continue
            add_ebook(content_path)
        else:
            print(f"Directory: {content_path}")
            add_ebook_recursive(content_path)


def add_ebook(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    # get ebook type
    mime_type, _ = mimetypes.guess_type(file_path)

    # add ebook to library
    if mime_type == EbookTypes.EPUB.value:
        meta_data = epub_meta.get_epub_metadata(file_path)
        authors = ",".join(meta_data.authors) or "Unknown"
        title = meta_data.title.replace("/", " ") or "Unknown"
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


def get_book_info(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == EbookTypes.EPUB.value:
        meta_data = epub_meta.get_epub_metadata(file_path)
        title = meta_data.title.replace("/", " ") or "Unknown"
        authors = ",".join(meta_data.authors) or "Unknown"
        size = meta_data.file_size_in_bytes / (1024 * 1024) or "Unknown"
        publisher = meta_data.publisher or "Unknown"
        published = "Unknown"
        if meta_data.publication_date:
            date = datetime.fromisoformat(meta_data.publication_date.split("T")[0])
            published = date.strftime("%b %Y")
        return title, authors, size, publisher, published

    if mime_type == EbookTypes.PDF.value:
        meta_data = PdfReader(file_path).metadata
        title = meta_data.title.replace("/", " ") or "Unknown"
        authors = meta_data.author or "Unknown"
        size = Path(file_path).stat().st_size / (1024 * 1024) or "Unknown"
        publisher = meta_data.creator or meta_data.producer or "Unknown"
        published = "Unknown"
        if meta_data.creation_date:
            date = meta_data.creation_date
            published = date.strftime("%b %Y")
        return title, authors, size, publisher, published
