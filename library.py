from constant import LIB_PATH, TABLE_HEADING
from lib_functions import get_books
from textual.app import App, ComposeResult
from textual.widgets import DataTable

lib_content = get_books(LIB_PATH)


class Library(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*TABLE_HEADING)
        if lib_content:
            table.add_rows(lib_content)
