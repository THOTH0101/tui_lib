import argparse

from constant import LIB_PATH
from functions.lib_get_content import get_lib_content
from functions.lib_add_content import add_ebook_recursive
from functions.lib_remove_content import remove_ebook, remove_ebook_recursive
from library import Library


def main():
    parser = argparse.ArgumentParser(description="TUI Library")

    parser.add_argument(
        "--add", type=str, help="add ebook to library using absolute path"
    )
    parser.add_argument(
        "--remove", type=str, help="remove ebook from library using 'title - author(s)'"
    )
    parser.add_argument(
        "--remove_all", action="store_true", help="remove all ebook from library"
    )
    parser.add_argument(
        "--list", action="store_true", help="print all ebook in library with author"
    )
    args = parser.parse_args()

    # cli commands logic
    if args.add:
        message = add_ebook_recursive(args.add)
        print(message)
        exit(0)

    if args.remove:
        sections = args.remove.split("-")
        message = "Error: invalid argument use --remove 'title - author(s)'"

        if len(sections) == 2:
            file_path = f"{LIB_PATH}/{sections[1].strip()}/{sections[0].strip()}"
            message = remove_ebook(file_path)
        print(message)
        exit(0)

    if args.remove_all:
        print(remove_ebook_recursive())
        exit(0)

    if args.list:
        books = get_lib_content()
        print(f"# Library Content: {len(books)} ebook(s)")
        for book in books:
            print(f" * {book[0]} - {book[1]}")
        exit(0)

    # start tui
    lib = Library()
    lib.run()


if __name__ == "__main__":
    main()
