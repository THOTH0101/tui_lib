from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class ConfirmationDialog(ModalScreen[bool]):
    BINDINGS = [
        ("escape", "close_modal", "Close current modal screen"),
    ]

    def __init__(self, question: str) -> None:
        self.question = question
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(self.question, id="question"),
            OptionList(
                Option("1. Yes", id="yes"),
                Option("2. No", id="no"),
                id="confirm_options",
            ),
            id="dialog",
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

    def action_close_modal(self):
        self.dismiss(None)
