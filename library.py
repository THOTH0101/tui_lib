from itertools import cycle
from rich.text import Text
from constant import LIB_PATH, TABLE_HEADING
from lib_functions import get_books, remove_ebook, remove_ebook_recursive
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.widgets import Footer, Header


cursors = cycle(["row"])
lib_content = get_books(LIB_PATH)


class Library(App):
    BINDINGS = [
        ("a", "add_ebook", "Add ebook file or folder"),
        ("d", "delete_ebook", "Delete hightlighted ebook"),
        ("D", "delete_all_ebooks", "Delete all ebooks"),
        ("k", "cursor_up", "Cursor up"),
        ("j", "cursor_down", "Cursor down"),
        ("t", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        table.add_columns(*TABLE_HEADING)
        if lib_content:
            # table.add_rows(lib_content)
            for number, row in enumerate(lib_content, start=1):
                label = Text(str(number), style="#B0FC38 italic")
                table.add_row(*row, label=label)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_cursor_up(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_up()

    def action_cursor_down(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_down()

    def action_delete_all_ebooks(self) -> None:
        table = self.query_one(DataTable)
        remove_ebook_recursive()
        table.clear()

    def action_delete_ebook(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)

        row_data = table.get_row(row_key)
        file_path = f"{LIB_PATH}/{row_data[1]}/{row_data[0]}"

        remove_ebook(file_path)
        table.remove_row(row_key)
