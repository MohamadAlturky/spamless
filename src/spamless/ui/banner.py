from typing import Iterator

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from spamless.ui.theme import (
    BRAND_COLOR,
    SECONDARY_COLOR,
    MUTED_COLOR,
    SUCCESS_STYLE,
)


def _header(console: Console, title: str, color: str = "cyan") -> None:
    """Print a compact section header with a left-accent bar instead of a full rule."""
    console.print(f"  [bold {color}]▎ {title}[/bold {color}]", highlight=False)

_LOGO = r"""
  ███████╗██████╗  █████╗ ███╗   ███╗██╗     ███████╗███████╗███████╗
  ██╔════╝██╔══██╗██╔══██╗████╗ ████║██║     ██╔════╝██╔════╝██╔════╝
  ███████╗██████╔╝███████║██╔████╔██║██║     █████╗  ███████╗███████╗
  ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║     ██╔══╝  ╚════██║╚════██║
  ███████║██║     ██║  ██║██║ ╚═╝ ██║███████╗███████╗███████║███████║
  ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
"""


def show_plan(context: str, clarifications: str, filename: str, console: Console) -> None:
    """Render context and clarifications as stacked sections."""
    console.print()

    _header(console, f"Context — {filename}", "cyan")
    console.print()
    ctx_content = Markdown(context) if context.strip() else Text("  Nothing confirmed yet.", style="dim")
    console.print(ctx_content)
    console.print()

    if clarifications.strip():
        _header(console, "Clarifications", "yellow")
        console.print()
        console.print(Markdown(clarifications))
        console.print()


def show_full_state(
    user_msg: str,
    answer: str,
    context: str,
    clarifications: str,
    filename: str,
    console: Console,
) -> None:
    """After each turn: show question, answer, then context and clarifications as stacked sections."""
    console.print()
    _header(console, "Question", "white")
    console.print()
    console.print(Text(f"  {user_msg}", style="white"))
    console.print()

    _header(console, "Answer", "cyan")
    console.print()
    console.print(Markdown(answer))
    console.print()

    _header(console, f"Context — {filename}", "cyan")
    console.print()
    ctx_content = Markdown(context) if context.strip() else Text("  Nothing confirmed yet.", style="dim")
    console.print(ctx_content)
    console.print()

    if clarifications.strip():
        _header(console, "Clarifications", "yellow")
        console.print()
        console.print(Markdown(clarifications))
        console.print()


def show_banner(console: Console) -> None:
    console.print(_LOGO, style=BRAND_COLOR)
    console.print()


def show_result(answer: str, choice: str, console: Console) -> None:
    console.print()
    _header(console, "Result", "green")
    console.print()
    console.print("  Topic:  ", style=MUTED_COLOR, end="")
    console.print(answer, style=SECONDARY_COLOR + " bold")
    console.print("  Action: ", style=MUTED_COLOR, end="")
    console.print(choice, style=SUCCESS_STYLE)
    console.print()


def show_ai_response(
    prompt: str,
    key_index: int,
    model: str,
    chunks: Iterator[str],
    console: Console,
) -> None:
    console.print()
    _header(console, "Request", "magenta")
    console.print()
    console.print("  Model:  ", style=MUTED_COLOR, end="")
    console.print(model, style=SECONDARY_COLOR + " bold")
    console.print("  Key:    ", style=MUTED_COLOR, end="")
    console.print(f"#{key_index}", style=SUCCESS_STYLE)
    console.print("  Input:  ", style=MUTED_COLOR, end="")
    console.print(prompt, style="white")
    console.print()
    _header(console, "Response", "cyan")
    console.print()

    full_text = ""
    with Live(console=console, refresh_per_second=15) as live:
        for chunk in chunks:
            full_text += chunk
            live.update(Text(full_text))
    console.print()
