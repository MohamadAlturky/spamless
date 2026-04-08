import questionary

from spamless.ui.theme import QUESTIONARY_STYLE

_FILTER_CHOICES = [
    "Block all",
    "Allow trusted",
    "Review manually",
    "Archive",
    "Ignore",
]

_MODE_CHOICES = [
    questionary.Choice("  Plan      build or refine a plan with AI", value="plan"),
    questionary.Choice("  Filter    ask AI what to filter", value="filter"),
]


def ask_mode() -> str:
    """Ask the user which mode to use. Returns 'plan' or 'filter'."""
    mode = questionary.select(
        "What would you like to do?",
        choices=_MODE_CHOICES,
        style=QUESTIONARY_STYLE,
    ).ask()
    return mode or "plan"


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
        choices=_FILTER_CHOICES,
        style=QUESTIONARY_STYLE,
        instruction=instruction,
    ).ask()
    return choice or ""
