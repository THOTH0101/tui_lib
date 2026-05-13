import os
import shutil
import epub_meta
import mimetypes

from constant import LIB_PATH, EbookTypes
from functions.helper_functions import is_valid_ebook
from pypdf import PdfReader


def add_ebook_recursive(file_path):
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    # if is a file it a single ebook return
    if os.path.isfile(file_path):
        return add_ebook(file_path)

    # if it's a directory, add every file in subdirectories
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

    mime_type, _ = mimetypes.guess_type(file_path)

    # add epub ebook to library directory
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

    # add pdf ebook to library directory
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
