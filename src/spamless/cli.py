import os
from rich.console import Console

from spamless.api.openrouter import stream_completion
from spamless.ui.banner import show_banner, show_ai_response
from spamless.prompts.questions import ask_mode, ask_question
from spamless.planner.session import run_planner_session

console = Console()


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        show_banner(console)

        mode = ask_mode()

        if mode == "plan":
            run_planner_session(console)
        else:
            answer = ask_question()
            if not answer:
                console.print("\n[dim]Nothing to filter. Goodbye.[/dim]\n")
                return
            key_index, model, chunks = stream_completion(answer)
            show_ai_response(answer, key_index, model, chunks, console)
    except KeyboardInterrupt:
        console.print("\n\n[bold magenta]  Goodbye from spamless.[/bold magenta]\n")
