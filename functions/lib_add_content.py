import os
from pathlib import Path
import shutil
import epub_meta
import mimetypes

from constant import LIB_PATH, EbookTypes
from functions.helper_functions import is_valid_ebook, sanitize_path_part
from pypdf import PdfReader


def add_ebook_recursive(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    # if is a file it a single ebook return
    if os.path.isfile(file_path):
        return add_ebook(file_path)

    # if it's a directory, add every file in subdirectories
    for root, _, files in os.walk(file_path):
        abs_root = os.path.abspath(root)
        abs_lib = os.path.abspath(LIB_PATH)

        # prevent the app from recursively scanning its own destination directory!
        if os.path.commonpath([abs_root, abs_lib]) == os.path.abspath(LIB_PATH):
            continue

        for file in files:
            full_path = os.path.join(root, file)
            if is_valid_ebook(full_path):
                print(add_ebook(full_path))

    return "Success: all ebook added"


def add_ebook(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist"

    mime_type, _ = mimetypes.guess_type(file_path)
    authors = "Unknown"
    title = "Unknown"
    extension = ""

    try:
        # add epub ebook to library directory
        if mime_type == EbookTypes.EPUB.value:
            extension = ".epub"
            meta_data = epub_meta.get_epub_metadata(file_path)
            if meta_data.authors:
                authors = (",".join(meta_data.authors)).strip()
            if meta_data.title:
                title = meta_data.title.strip()

        # add pdf ebook to library directory
        elif mime_type == EbookTypes.PDF.value:
            extension = ".pdf"
            meta_data = PdfReader(file_path).metadata
            authors = meta_data.get("/Author", "Unknown")
            title = meta_data.get("/Title", "Unknown")

        else:
            return "Error: invalid ebook type"

        # sanitize and construct path
        safe_author = sanitize_path_part(str(authors))
        safe_title = sanitize_path_part(str(title))
        final_dir = Path(LIB_PATH) / safe_author / safe_title
        dest_path = final_dir / f"{safe_title} - {safe_author}{extension}"

        print(f"Copying ebook file from {file_path} to {dest_path}")
        final_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, dest_path)
        return f"Success: {file_path} added"

    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"
