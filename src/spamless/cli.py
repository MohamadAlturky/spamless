import os
from rich.console import Console

from spamless.ui.banner import show_banner, show_result
from spamless.prompts.questions import ask_question, show_select

console = Console()


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        show_banner(console)
        answer = ask_question()
        if not answer:
            console.print("\n[dim]Nothing to filter. Goodbye.[/dim]\n")
            return
        choice = show_select(answer)
        if not choice:
            console.print("\n[dim]No action selected. Goodbye.[/dim]\n")
            return
        show_result(answer, choice, console)
    except KeyboardInterrupt:
        console.print("\n\n[bold magenta]  Goodbye from spamless.[/bold magenta]\n")
