import argparse

from library import Library
from lib_functions import add_ebook_recursive


def main():
    parser = argparse.ArgumentParser(description="TUI Library")
    parser.add_argument("--path", type=str, help="path to ebook file or directory")
    args = parser.parse_args()

    if args.path:
        add_ebook_recursive(args.path)
        exit(0)

    lib = Library()
    lib.run()


if __name__ == "__main__":
    main()
