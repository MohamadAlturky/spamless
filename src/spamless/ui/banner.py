from typing import Iterator

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.table import Table
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
    """Render context and clarifications side by side."""
    console.print()

    ctx_content = Markdown(context) if context.strip() else Text("Nothing confirmed yet.", style="dim")
    clar_content = Markdown(clarifications) if clarifications.strip() else Text("", style="dim")

    grid = Table.grid(padding=(0, 3), expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    # headers row
    grid.add_row(
        Text(f"▎ Context — {filename}", style="bold cyan"),
        Text("▎ Clarifications", style="bold yellow") if clarifications.strip() else Text(""),
    )
    # content row
    grid.add_row(ctx_content, clar_content)

    console.print(grid)
    console.print()


def show_full_state(
    user_msg: str,
    answer: str,
    context: str,
    clarifications: str,
    filename: str,
    console: Console,
) -> None:
    """After each turn: show question, answer, then context + clarifications side by side."""
    qa_grid = Table.grid(padding=(0, 3), expand=True)
    qa_grid.add_column(ratio=1)
    qa_grid.add_column(ratio=1)
    qa_grid.add_row(
        Text("▎ Question", style="bold white"),
        Text("▎ Answer", style="bold cyan"),
    )
    qa_grid.add_row(
        Text(user_msg, style="white"),
        Markdown(answer),
    )
    console.print()
    console.print(qa_grid)
    console.print()

    ctx_content = Markdown(context) if context.strip() else Text("Nothing confirmed yet.", style="dim")
    clar_content = Markdown(clarifications) if clarifications.strip() else Text("", style="dim")

    grid = Table.grid(padding=(0, 3), expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    grid.add_row(
        Text(f"▎ Context — {filename}", style="bold cyan"),
        Text("▎ Clarifications", style="bold yellow") if clarifications.strip() else Text(""),
    )
    grid.add_row(ctx_content, clar_content)

    console.print(grid)
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
