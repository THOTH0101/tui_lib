import mimetypes
import os
from pathlib import Path

from constant import LIB_PATH


def format_long_str(text: str) -> str:
    default_len = 40
    if len(text) > default_len:
        return f"{text[:default_len]}..."
    return text


def sanitize_path_part(part: str) -> str:
    chars_to_remove = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for char in chars_to_remove:
        part = part.replace(char, " ")
    return part.strip()


def remove_lib_empty_dirs() -> None:
    abs_lib = os.path.abspath(LIB_PATH)
    if not os.path.exists(abs_lib):
        return

    # process child directories before parents
    for root, _, _ in os.walk(abs_lib, topdown=False):
        if os.path.abspath(root) == abs_lib:
            continue

        if not os.listdir(root):
            try:
                os.rmdir(root)
            except Exception as e:
                print(f"Could not remove directory {root}: {e}")


def is_ebook_extension(file_path: Path) -> bool:
    SUPPORTED_EXTENSIONS = {".epub", ".pdf", ".mobi", ".azw3", ".fb2"}

    return Path(file_path).suffix.lower() in SUPPORTED_EXTENSIONS


def is_valid_ebook(file_path: str) -> bool:
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
