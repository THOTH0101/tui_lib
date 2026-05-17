import os
import platform
import subprocess
from pathlib import Path


def open_ebook(file_path: str) -> tuple[bool, str]:
    """Launches the system default application to open a file on Linux, Windows, or macOS."""
    path = Path(file_path).resolve()

    if not path.exists():
        return False, f"Error: File does not exist at {file_path}"

    if not path.is_file():
        return False, "Error: Selected path is a directory."

    current_os = platform.system().lower()

    try:
        if current_os == "windows":
            # on windows, 'start' requires shell=True because it's a cmd built-in.
            # passing an empty string "" as the first argument prevents paths with spaces
            # from being misinterpreted as window titles.
            subprocess.Popen(
                f'start "" "{path}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif current_os == "darwin":  # macOS
            subprocess.Popen(
                ["open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:  # Linux / Unix fallback
            subprocess.Popen(
                ["xdg-open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=getattr(
                    os, "setsid", None
                ),  # Safe fallback if setsid missing
            )

        return True, f"Opening '{path.name}'..."

    except Exception as e:
        return False, f"Failed to open file: {str(e)}"
