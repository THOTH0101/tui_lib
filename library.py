from functions.lib_open_content import open_ebook
from textual import work
from dialog import ConfirmationDialog
from functions.lib_add_content import add_ebook_recursive
from functions.lib_get_content import get_lib_content
from functions.lib_remove_content import remove_ebook, remove_ebook_recursive
from input import TextInput
from rich.text import Text
from constant import TABLE_HEADING
from textual.app import App, ComposeResult
from textual.widgets import DataTable, LoadingIndicator, Footer, Header


class Library(App):
    CSS_PATH = "library.tcss"
    BINDINGS = [
        ("a", "add_ebook", "Add ebook file or folder"),
        ("d", "delete_ebook", "Delete hightlighted ebook"),
        ("D", "delete_all_ebooks", "Delete all ebooks"),
        ("k", "cursor_up", "Cursor up"),
        ("j", "cursor_down", "Cursor down"),
        ("l", "cursor_right", "Cursor right"),
        ("h", "cursor_left", "Cursor left"),
        ("t", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator(id="loader")
        yield DataTable(id="content_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#content_table")
        table.display = False
        table.add_columns(*TABLE_HEADING)
        table.cursor_type = "row"
        self.sync_lib_content()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        file_path = event.row_key.value

        if file_path:
            success, message = open_ebook(file_path)
            self.notify(message, severity="info" if success else "error")

    @work(exclusive=True, thread=True)
    def sync_lib_content(self, current_index: int = 0):
        table = self.query_one(DataTable)
        self.query_one("#loader").display = True
        table.display = False
        contents = get_lib_content()

        # using call_from_thread to update because we are in a worker thread
        def update_ui():
            table.clear()
            if contents:
                for number, row in enumerate(contents, start=1):
                    display_row = row[:5]
                    file_path = row[5]
                    label = Text(str(number), style="#B0FC38 italic")
                    table.add_row(*display_row, label=label, key=file_path)

            if table.row_count > 0:
                # ensure index isn't out of range
                safe_index = min(current_index, table.row_count - 1)
                # move cursor to Coordinate(row_index, column_index)
                table.move_cursor(row=safe_index, animate=False)
            self.query_one("#loader").display = False
            table.display = True

        self.call_from_thread(update_ui)

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

    def action_cursor_right(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_right()

    def action_cursor_left(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_left()

    def action_add_ebook(self) -> None:
        def check_input(text: str):
            if text:
                file_path = text.strip()
                message = add_ebook_recursive(file_path)
                self.sync_lib_content()
                self.notify(message)

        self.push_screen(TextInput("Enter ebook file path:", "File path"), check_input)

    def action_delete_all_ebooks(self) -> None:
        def confirm_check(should_delete: bool):
            if should_delete:
                message = remove_ebook_recursive()
                self.sync_lib_content()
                self.notify(message)

        self.push_screen(
            ConfirmationDialog("Are you sure you want to delete all ebook?"),
            confirm_check,
        )

    def action_delete_ebook(self) -> None:
        table = self.query_one(DataTable)

        def confirm_check(should_delete: bool):
            if should_delete:
                row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
                file_path = row_key.value
                current_row_index = table.get_row_index(row_key)
                total_rows = table.row_count
                target_row_index = current_row_index

                if current_row_index == total_rows - 1 and total_rows > 1:
                    target_row_index = current_row_index - 1
                message = remove_ebook(file_path)
                self.sync_lib_content(current_index=target_row_index)
                self.notify(message)

        self.push_screen(
            ConfirmationDialog("Are you sure you want to delete this ebook?"),
            confirm_check,
        )
