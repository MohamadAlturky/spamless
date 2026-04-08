import questionary

from spamless.ui.theme import QUESTIONARY_STYLE


def ask_user_message() -> str | None:
    """Prompt for next user message. Returns None on empty input (signals quit)."""
    msg = questionary.text(
        "You →",
        instruction="(empty to quit)",
        style=QUESTIONARY_STYLE,
    ).ask()
    if msg is None or msg.strip() == "":
        return None
    return msg.strip()


def ask_accept_diff() -> bool:
    """Ask user to accept or reject proposed plan changes."""
    return questionary.confirm(
        "Accept proposed plan changes?",
        default=True,
        style=QUESTIONARY_STYLE,
    ).ask()
