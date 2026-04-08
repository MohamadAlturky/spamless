from typing import Iterator

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
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


def show_plan(context: str, clarifications: str, filename: str, console: Console) -> None:
    """Render context and clarifications as two distinct panels."""
    console.print()

    ctx_body = Markdown(context) if context.strip() else Text("Nothing confirmed yet.", style="dim")
    console.print(
        Panel(
            ctx_body,
            title=f"[bold cyan] Context — {filename} [/bold cyan]",
            border_style=SECONDARY_COLOR,
            padding=(1, 2),
        )
    )

    if clarifications.strip():
        console.print(
            Panel(
                Markdown(clarifications),
                title="[bold yellow] Clarifications Needed [/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )

    console.print()


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


def show_ai_response(
    prompt: str,
    key_index: int,
    model: str,
    chunks: Iterator[str],
    console: Console,
) -> None:
    request_content = Text()
    request_content.append("  Model:  ", style=MUTED_COLOR)
    request_content.append(f"{model}\n", style=SECONDARY_COLOR + " bold")
    request_content.append("  Key:    ", style=MUTED_COLOR)
    request_content.append(f"#{key_index}\n", style=SUCCESS_STYLE)
    request_content.append("  Input:  ", style=MUTED_COLOR)
    request_content.append(prompt, style="white")

    console.print()
    console.print(
        Panel(
            request_content,
            title="[bold magenta] Request [/bold magenta]",
            border_style=BRAND_COLOR,
            padding=(1, 2),
            expand=False,
        )
    )
    console.print()

    full_text = ""
    with Live(console=console, refresh_per_second=15) as live:
        for chunk in chunks:
            full_text += chunk
            live.update(
                Panel(
                    full_text,
                    title="[bold cyan] Response [/bold cyan]",
                    border_style=SECONDARY_COLOR,
                    padding=(1, 2),
                )
            )
    console.print()
