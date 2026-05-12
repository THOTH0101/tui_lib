from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Input, Label


class TextInput(ModalScreen[str]):
    BINDINGS = [
        ("escape", "close_modal", "Close current modal screen"),
    ]

    def __init__(self, question: str, placeholder: str) -> None:
        self.question = question
        self.placeholder = placeholder
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(self.question, id="question"),
            Input(placeholder=self.placeholder, type="text", id="input"),
            id="dialog",
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.value:
            self.dismiss(event.input.value)
        else:
            self.dismiss(None)

    def action_close_modal(self):
        self.dismiss(None)
