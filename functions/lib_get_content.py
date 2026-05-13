import mimetypes
import os
from pathlib import Path
from constant import LIB_PATH, EbookTypes
import epub_meta

from datetime import datetime
from functions.helper_functions import is_valid_ebook
from pypdf import PdfReader


def get_lib_content():
    return get_books_recursive(LIB_PATH)


def get_book_info(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    # extract epub ebook metadata
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

    # extract pdf ebook metadata
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


def get_books_recursive(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        return

    # get library content
    book_list = []
    contents = os.listdir(file_path)
    for content in contents:
        content_path = os.path.join(file_path, content)
        if os.path.isfile(content_path):
            # add only valid ebook
            if not is_valid_ebook(content_path):
                continue
            book_list.append(get_book_info(content_path))
        else:
            # scan subdirectory
            new_list = get_books_recursive(content_path)
            if new_list:
                book_list.extend(new_list)
    return book_list
