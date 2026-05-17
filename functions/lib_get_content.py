import mimetypes
import os
from pathlib import Path
from constant import LIB_PATH, EbookTypes
import epub_meta

from datetime import datetime
from functions.helper_functions import is_valid_ebook
from pypdf import PdfReader


def get_lib_content() -> list:
    return get_books_recursive(LIB_PATH)


def get_books_recursive(file_path: str) -> list:
    abs_target = os.path.abspath(file_path)

    if not os.path.exists(abs_target):
        os.makedirs(abs_target, exist_ok=True)
        return []

    book_list = []

    # get library content
    for root, _, files in os.walk(abs_target):
        for file in files:
            content_path = os.path.join(root, file)

            # Filter for valid extensions (.epub, .pdf)
            if is_valid_ebook(content_path):
                try:
                    book_info = get_book_info(content_path)
                    if book_info:
                        book_list.append(book_info)
                except Exception as e:
                    # skip corrupted metadata structure
                    print(f"Skipping unreadable book metadata at {content_path}: {e}")
                    continue

    return book_list


def get_book_info(file_path: str) -> tuple | str:
    path = Path(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    file_size_mb = round(path.stat().st_size / (1024 * 1024), 2)
    title, authors, publisher, published = "Unknown", "Unknown", "Unknown", "Unknown"

    try:
        # extract pdf ebook metadata
        if mime_type == EbookTypes.EPUB.value:
            meta_data = epub_meta.get_epub_metadata(file_path)
            if meta_data.title:
                title = meta_data.title.replace("/", " ").strip()

            if meta_data.authors:
                authors = (",".join(meta_data.authors)).strip()

            if meta_data.publisher:
                publisher = meta_data.publisher

            if meta_data.publication_date:
                try:
                    date_str = meta_data.publication_date.split("T")[0]
                    published = datetime.fromisoformat(date_str).strftime("%b %Y")
                except ValueError:
                    published = "Unknown"

        # extract pdf ebook metadata
        elif mime_type == EbookTypes.PDF.value:
            meta_data = PdfReader(file_path).metadata

            title = meta_data.get("/Title", "Unknown").replace("/", " ").strip()
            authors = meta_data.get("/Author", "Unknown").strip()
            publisher_raw = meta_data.get("/Creator", "Unknown")
            if hasattr(publisher_raw, "get_object"):
                publisher = str(publisher_raw.get_object())
            else:
                publisher = str(publisher_raw)

            # pdf dates require special parsing (e.g., D:20230514)
            creation_date = meta_data.get("/CreationDate")
            if creation_date:
                # basic pdf date string slice: D:YYYYMMDD...
                try:
                    date_part = str(creation_date).replace("D:", "")[:8]
                    published = datetime.strptime(date_part, "%Y%m%d").strftime("%b %Y")
                except (ValueError, IndexError):
                    published = "Unknown"

    except Exception as e:
        return f"Error parsing metadata for {file_path}: {e}"

    return title, authors, file_size_mb, publisher, published, file_path
