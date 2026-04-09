import os

from rich.console import Console

from spamless import db
from spamless.ui.banner import show_banner
from spamless.ui.plans_page import run_plans_page
from spamless.planner.session import run_planner_session

console = Console()


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        show_banner(console)
        db.init_db()

        while True:
            action, plan_id = run_plans_page(console)

            if action == "quit":
                console.print("\n[bold magenta]  Goodbye from spamless.[/bold magenta]\n")
                return

            run_planner_session(console, plan_id)

    except KeyboardInterrupt:
        console.print("\n\n[bold magenta]  Goodbye from spamless.[/bold magenta]\n")
