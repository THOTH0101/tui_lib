from itertools import cycle
from constant import TABLE_HEADING
from functions.lib_get_content import get_lib_content
from rich.text import Text

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


class Table(Widget):
    content = reactive(get_lib_content, recompose=True)

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = next(cycle(["row"]))
        table.add_columns(*TABLE_HEADING)
        if self.content:
            for number, row in enumerate(self.content, start=1):
                label = Text(str(number), style="#B0FC38 italic")
                table.add_row(*row, label=label)
