import argparse

from functions.lib_get_content import get_lib_content
from functions.lib_add_content import add_ebook_recursive
from functions.lib_remove_content import remove_ebook, remove_ebook_recursive
from library import Library


def main():
    parser = argparse.ArgumentParser(description="TUI Library")

    parser.add_argument(
        "--add", type=str, help="add ebook(s) to library using absolute path"
    )
    parser.add_argument(
        "--remove", type=str, help="remove ebook from library using ebook path"
    )
    parser.add_argument(
        "--remove_all", action="store_true", help="remove all ebooks from library"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print all ebook in library with author(s) and path",
    )
    args = parser.parse_args()

    # cli commands logic
    if args.add:
        message = add_ebook_recursive(args.add)
        print(message)
        exit(0)

    if args.remove:
        file_path = args.remove
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
            print(f" * {book[0]} - {book[1]}\n   Path: {book[5]}")
        exit(0)

    # start tui
    lib = Library()
    lib.run()


if __name__ == "__main__":
    main()
