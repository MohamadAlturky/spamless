from rich.console import Console

from spamless.planner.ai import stream_plan_response
from spamless.planner.diff import show_diff
from spamless.planner.io import load_plan, save_plan
from spamless.planner.prompts import ask_accept_diff, ask_plan_name, ask_user_message
from spamless.ui.banner import show_plan


def run_planner_session(console: Console) -> None:
    """Interactive planning loop: load/create plan → converse → diff/accept → save."""
    path = ask_plan_name()
    context, clarifications = load_plan(path)
    show_plan(context, clarifications, path.name, console)

    while True:
        user_msg = ask_user_message()
        if user_msg is None:
            console.print("\n[dim]Goodbye.[/dim]\n")
            break

        _answer, new_ctx, new_clar = stream_plan_response(
            context, clarifications, user_msg, console
        )

        ctx_changed = new_ctx is not None and new_ctx.strip() != context.strip()
        clar_changed = new_clar is not None and new_clar.strip() != clarifications.strip()

        if ctx_changed or clar_changed:
            console.print()
            if ctx_changed:
                show_diff(context, new_ctx, console, label="Context Changes")
            if clar_changed:
                show_diff(clarifications, new_clar, console, label="Clarifications Changes")

            if ask_accept_diff():
                if ctx_changed:
                    context = new_ctx
                if clar_changed:
                    clarifications = new_clar
                save_plan(path, context, clarifications)
                show_plan(context, clarifications, path.name, console)
            else:
                console.print("[dim]Plan unchanged.[/dim]\n")
