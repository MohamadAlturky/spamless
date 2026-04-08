from pathlib import Path

import questionary

from spamless.ui.theme import QUESTIONARY_STYLE


def ask_plan_name() -> Path:
    """Prompt for plan name. Autocompletes from existing .md files in CWD."""
    existing = [p.stem for p in Path.cwd().glob("*.md")]
    if existing:
        name = questionary.autocomplete(
            "Plan name:",
            choices=existing,
            style=QUESTIONARY_STYLE,
        ).ask()
    else:
        name = questionary.text(
            "Plan name:",
            style=QUESTIONARY_STYLE,
        ).ask()
    if not name:
        name = "plan"
    if not name.endswith(".md"):
        name = f"{name}.md"
    return Path.cwd() / name


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
