import questionary

from spamless.ui.theme import QUESTIONARY_STYLE

_CHOICES = [
    "Block all",
    "Allow trusted",
    "Review manually",
    "Archive",
    "Ignore",
]


def ask_question() -> str:
    answer = questionary.text(
        "What should spamless filter?",
        style=QUESTIONARY_STYLE,
    ).ask()
    return answer or ""


def show_select(context: str) -> str:
    instruction = f"(filtering: {context})" if context else ""
    choice = questionary.select(
        "How should spamless handle this?",
        choices=_CHOICES,
        style=QUESTIONARY_STYLE,
        instruction=instruction,
    ).ask()
    return choice or ""
