# 📚 TuiLib (TUI E-Book Manager) in Python

TuiLib is a lightweight, keyboard-centric terminal user interface (TUI) application for managing your digital library. It aims to provide a "Vim-like" experience 😎 for users who prefer staying in the terminal rather than using heavy GUI applications to manage their E-Book.

## ⚠️ Disclaimer

This personal project was intended to serve as a medium to express the use of programming language, file operations at the OS level, system design, and version control. The application is not optimised for optimal performance. Feel free to fork and improve to suit more personalized use.

## 🖼️ Screenshots

- Lightmode
  <img width="1080" height="680" alt="app_screenshot" src="https://github.com/user-attachments/assets/aaeeaef5-8a31-4952-b76e-f46869a989bc" />

- Darkmode
  <img width="1080" height="680" alt="app_screenshot1" src="https://github.com/user-attachments/assets/2a8aa58e-f0d7-4ee7-b71f-c8b63c1cbd48" />

## ⚒ Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [uv Package Manager](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

1. Clone the repo:

```
git clone https://github.com/THOTH0101/tui_lib.git
```

2. Install dependencies in uv.lock and set up a virtual environment using the uv command:

```
uv sync
```

3. Start the program in TUI:

```
uv run main.py
```

### Cli Commands

- To view available commands and usage

```
uv run main.py -h
```

- To add an ebook using the absolute path of files and folders

```
uv run main.py --add <absolute_path>
```

- To delete a specific ebook:

```
uv run main.py --remove <tuilib_ebook_path>
```

- To delete all the ebooks in the library:

```
uv run main.py --remove_all
```

- To list all the ebooks in the library with their author(s) and tuilib path:

```
uv run main.py --list
```

---

NB: the app might take a while to respond(or even look stuck) when adding ebooks via the TUI, and loading a large amount of ebooks will take time to load the UI.
Thanks for checking out the project 👍
