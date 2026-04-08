import questionary

from spamless.ui.theme import QUESTIONARY_STYLE

_FILTER_CHOICES = [
    "Block all",
    "Allow trusted",
    "Review manually",
    "Archive",
    "Ignore",
]


def show_select(context: str) -> str:
    instruction = f"(filtering: {context})" if context else ""
    choice = questionary.select(
        "How should spamless handle this?",
        choices=_FILTER_CHOICES,
        style=QUESTIONARY_STYLE,
        instruction=instruction,
    ).ask()
    return choice or ""
