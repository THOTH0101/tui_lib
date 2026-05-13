from enum import Enum
import os


LIB_PATH = os.path.join("./", "TUI Library")

TABLE_HEADING = ("Title", "Author(s)", "Size(mb)", "Publisher", "Published")


class EbookTypes(Enum):
    EPUB = "application/epub+zip"
    PDF = "application/pdf"
