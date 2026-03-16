from components.library import Library
from library_operations import get_lib_content


def main():
    # lib = Library()
    # lib.run()
    lib_content = get_lib_content()
    print(lib_content)


if __name__ == "__main__":
    main()
