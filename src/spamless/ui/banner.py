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

_LOGO = r"""
  ███████╗██████╗  █████╗ ███╗   ███╗██╗     ███████╗███████╗███████╗
  ██╔════╝██╔══██╗██╔══██╗████╗ ████║██║     ██╔════╝██╔════╝██╔════╝
  ███████╗██████╔╝███████║██╔████╔██║██║     █████╗  ███████╗███████╗
  ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║     ██╔══╝  ╚════██║╚════██║
  ███████║██║     ██║  ██║██║ ╚═╝ ██║███████╗███████╗███████║███████║
  ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
"""


def show_plan(context: str, clarifications: str, filename: str, console: Console) -> None:
    """Render context and clarifications as plain sections."""
    console.print()
    console.rule(f"[bold cyan]Context — {filename}[/bold cyan]", style="cyan")
    console.print()
    if context.strip():
        console.print(Markdown(context))
    else:
        console.print("  Nothing confirmed yet.", style="dim")
    console.print()

    if clarifications.strip():
        console.rule("[bold yellow]Clarifications[/bold yellow]", style="yellow")
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
    """After each turn: show question, answer, context, clarifications."""
    console.print()
    console.rule("[bold white]Question[/bold white]", style="dim")
    console.print()
    console.print(f"  {user_msg}", style="white")
    console.print()
    console.rule("[bold cyan]Answer[/bold cyan]", style="cyan")
    console.print()
    console.print(Markdown(answer))
    console.print()
    console.rule(f"[bold cyan]Context — {filename}[/bold cyan]", style="cyan")
    console.print()
    if context.strip():
        console.print(Markdown(context))
    else:
        console.print("  Nothing confirmed yet.", style="dim")
    console.print()
    if clarifications.strip():
        console.rule("[bold yellow]Clarifications[/bold yellow]", style="yellow")
        console.print()
        console.print(Markdown(clarifications))
        console.print()


def show_banner(console: Console) -> None:
    console.print(_LOGO, style=BRAND_COLOR)
    console.print()


def show_result(answer: str, choice: str, console: Console) -> None:
    console.print()
    console.rule("[bold green]Result[/bold green]", style="green")
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
    console.rule("[bold magenta]Request[/bold magenta]", style="magenta")
    console.print()
    console.print("  Model:  ", style=MUTED_COLOR, end="")
    console.print(model, style=SECONDARY_COLOR + " bold")
    console.print("  Key:    ", style=MUTED_COLOR, end="")
    console.print(f"#{key_index}", style=SUCCESS_STYLE)
    console.print("  Input:  ", style=MUTED_COLOR, end="")
    console.print(prompt, style="white")
    console.print()
    console.rule("[bold cyan]Response[/bold cyan]", style="cyan")
    console.print()

    full_text = ""
    with Live(console=console, refresh_per_second=15) as live:
        for chunk in chunks:
            full_text += chunk
            live.update(Text(full_text))
    console.print()
