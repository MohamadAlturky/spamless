import os

from rich.console import Console

from spamless import db
from spamless.planner.ai import stream_plan_response
from spamless.planner.diff import show_diff
from spamless.planner.io import _build_markdown, _parse_sections
from spamless.planner.prompts import ask_accept_diff, ask_user_message
from spamless.ui.banner import show_full_state, show_plan


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def run_planner_session(console: Console, plan_id: int) -> None:
    """Interactive planning loop: load plan from DB → converse → diff/accept → save."""
    plan = db.get_plan(plan_id)
    if plan is None:
        console.print("[bold red]Plan not found.[/bold red]")
        return

    title = plan["title"]
    context, clarifications = _parse_sections(plan["content"])

    _clear()
    show_plan(context, clarifications, title, console)

    while True:
        user_msg = ask_user_message()
        if user_msg is None:
            console.print("\n[dim]Goodbye.[/dim]\n")
            break

        _clear()
        _answer, new_ctx, new_clar = stream_plan_response(
            context, clarifications, user_msg, console
        )

        ctx_changed = new_ctx is not None and new_ctx.strip() != context.strip()
        clar_changed = new_clar is not None and new_clar.strip() != clarifications.strip()

        if ctx_changed or clar_changed:
            if ctx_changed:
                show_diff(context, new_ctx, console, label="Context Changes")
            if clar_changed:
                show_diff(clarifications, new_clar, console, label="Clarifications Changes")

            if ask_accept_diff():
                if ctx_changed:
                    context = new_ctx
                if clar_changed:
                    clarifications = new_clar
                db.save_plan(plan_id, _build_markdown(context, clarifications))
            else:
                console.print("[dim]Plan unchanged.[/dim]\n")

        _clear()
        show_full_state(user_msg, _answer, context, clarifications, title, console)
