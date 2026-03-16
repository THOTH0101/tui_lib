from constant import TABLE_HEADING
from textual.app import App, ComposeResult
from textual.widgets import DataTable

books = [
    (
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "2023-10-01",
        "1.2 MB",
        "Scribner",
        "1925",
    ),
    (
        "Neuromancer",
        "William Gibson",
        "2023-11-15",
        "0.8 MB",
    ),
    ("Foundation", "Isaac Asimov", "2024-01-05", "1.5 MB", "Gnome Press", "1951"),
]


class Library(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*TABLE_HEADING)
        table.add_rows(books)
