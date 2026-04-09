import os
import subprocess
import sys

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text

from spamless import db
from spamless.ui.banner import _header
from spamless.ui.theme import BRAND_COLOR, QUESTIONARY_STYLE

PAGE_SIZE = 5


# ── key reading ────────────────────────────────────────────────────────────────

def _getch() -> str:
    """Read one logical key. Returns 'up', 'down', or a single character."""
    if sys.platform == "win32":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            return {"H": "up", "P": "down"}.get(ch2.decode("latin-1", errors="ignore"), "")
        return ch.decode("utf-8", errors="ignore")
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                rest = sys.stdin.read(2)
                return {"[A": "up", "[B": "down"}.get(rest, "")
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ── clipboard ──────────────────────────────────────────────────────────────────

def _copy(text: str) -> bool:
    try:
        if sys.platform == "win32":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        else:
            subprocess.run(
                ["xclip", "-selection", "clipboard"], input=text.encode(), check=True
            )
        return True
    except Exception:
        return False


# ── rendering ──────────────────────────────────────────────────────────────────

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _render(console: Console, plans: list[dict], selected: int, page: int, total: int, message: str) -> None:
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    console.print()
    _header(console, f"Plans  [dim]page {page}/{total_pages}[/dim]", "magenta")
    console.print()

    if not plans:
        console.print("  [dim]No plans yet. Press [bold]n[/bold] to create one.[/dim]")
        console.print()
    else:
        table = Table(show_header=True, header_style="bold dim", box=None, padding=(0, 2))
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", min_width=30)
        table.add_column("Created At", style="dim", width=20)

        for i, plan in enumerate(plans):
            is_selected = i == selected
            row_style = "bold cyan reverse" if is_selected else ""
            prefix = "▶ " if is_selected else "  "
            table.add_row(
                str(plan["id"]),
                f"{prefix}{plan['title']}",
                plan["created_at"][:16],
                style=row_style,
            )

        console.print(table)
        console.print()

    if message:
        console.print(f"  [bold green]{message}[/bold green]")
        console.print()

    console.print(
        "  [dim]↑↓ navigate   "
        "[bold]c[/bold] copy   "
        "[bold]d[/bold] details   "
        "[bold]enter[/bold] open   "
        "[bold]n[/bold] new   "
        "[bold]f[/bold] fork   "
        "[bold]x[/bold] delete   "
        "[bold]q[/bold] quit[/dim]"
    )
    console.print()


# ── main entry ─────────────────────────────────────────────────────────────────

def run_plans_page(console: Console) -> tuple[str, int | None]:
    """
    Interactive plans browser.
    Returns ("open", plan_id), ("new", None), or ("quit", None).
    """
    page = 1
    selected = 0
    message = ""

    while True:
        plans, total = db.list_plans(page, PAGE_SIZE)
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

        # clamp selection
        max_sel = max(0, len(plans) - 1)
        selected = min(selected, max_sel)

        _clear()
        console.print()
        console.print("  " + "  ", style=BRAND_COLOR, end="")
        _render(console, plans, selected, page, total, message)
        message = ""

        key = _getch()

        if key == "up":
            if selected > 0:
                selected -= 1
            elif page > 1:
                page -= 1
                selected = PAGE_SIZE - 1
        elif key == "down":
            if selected < len(plans) - 1:
                selected += 1
            elif page < total_pages:
                page += 1
                selected = 0
        elif key in ("\r", "\n"):
            if plans:
                return "open", plans[selected]["id"]
        elif key == "n":
            _clear()
            title = questionary.text(
                "Plan title:",
                style=QUESTIONARY_STYLE,
            ).ask()
            if title and title.strip():
                plan_id = db.create_plan(title.strip())
                return "new", plan_id
        elif key == "c":
            if plans:
                plan = db.get_plan(plans[selected]["id"])
                if plan and plan["content"]:
                    ok = _copy(plan["content"])
                    message = "Copied to clipboard." if ok else "Copy failed — no clipboard tool found."
                else:
                    message = "Plan has no content yet."
        elif key == "d":
            if plans:
                plan = db.get_plan(plans[selected]["id"])
                _clear()
                console.print()
                _header(console, plan["title"], "cyan")
                console.print(f"  [dim]id: {plan['id']}   created: {plan['created_at'][:16]}[/dim]")
                console.print()
                if plan["content"].strip():
                    console.print(Markdown(plan["content"]))
                else:
                    console.print("  [dim]No content yet.[/dim]")
                console.print()
                console.print("  [dim]Press any key to go back...[/dim]")
                _getch()
        elif key == "f":
            if plans:
                plan = plans[selected]
                _clear()
                new_title = questionary.text(
                    f"Fork \"{plan['title']}\" — new name:",
                    style=QUESTIONARY_STYLE,
                ).ask()
                if new_title and new_title.strip():
                    new_id = db.fork_plan(plan["id"], new_title.strip())
                    message = f"Forked as \"{new_title.strip()}\"."
        elif key == "x":
            if plans:
                plan = plans[selected]
                _clear()
                confirmed = questionary.confirm(
                    f"Delete \"{plan['title']}\"?",
                    default=False,
                    style=QUESTIONARY_STYLE,
                ).ask()
                if confirmed:
                    db.delete_plan(plan["id"])
                    selected = max(0, selected - 1)
                    message = f"Deleted \"{plan['title']}\"."
        elif key in ("q", "\x03", "\x1b"):
            return "quit", None
