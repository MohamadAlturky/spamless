from rich.console import Console
from rich.panel import Panel
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


def show_banner(console: Console) -> None:
    console.print(_LOGO, style=BRAND_COLOR)
    console.print()


def show_result(answer: str, choice: str, console: Console) -> None:
    console.print()

    content = Text()
    content.append("  Topic:   ", style=MUTED_COLOR)
    content.append(f"{answer}\n", style=SECONDARY_COLOR + " bold")
    content.append("  Action:  ", style=MUTED_COLOR)
    content.append(choice, style=SUCCESS_STYLE)

    console.print(
        Panel(
            content,
            title="[bold green] Result [/bold green]",
            border_style="green",
            padding=(1, 2),
            expand=False,
        )
    )
    console.print()
