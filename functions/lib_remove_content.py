from pathlib import Path
import shutil

from constant import LIB_PATH
from functions.helper_functions import remove_lib_empty_dirs


def remove_ebook_recursive() -> str:
    target_path = Path(LIB_PATH)

    if not target_path.exists() or not any(target_path.iterdir()):
        return "library is already empty"

    try:
        for item in target_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()

        # clear up the library
        remove_lib_empty_dirs()
        return "Success: all ebooks deleted"

    except Exception as e:
        return f"Error clearing library: {str(e)}"


def remove_ebook(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        return f"Error: {file_path} does not exist"

    try:
        if path.is_file():
            path.unlink()

        elif path.is_dir():
            shutil.rmtree(path)

        # clear up the library
        remove_lib_empty_dirs()
        return "Success: ebook deleted"

    except Exception as e:
        return f"Error deleting {path.name}: {str(e)}"
