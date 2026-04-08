import difflib

from rich.console import Console
from rich.syntax import Syntax


def show_diff(old: str, new: str, console: Console, label: str = "Proposed Changes") -> None:
    """Render a unified diff between old and new text using Rich."""
    if old.strip() == new.strip():
        return

    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff_lines = list(
        difflib.unified_diff(old_lines, new_lines, fromfile="current", tofile="proposed")
    )

    diff_text = "".join(diff_lines)
    syntax = Syntax(diff_text, "diff", theme="monokai", word_wrap=True)
    console.print()
    console.rule(f"[bold yellow]{label}[/bold yellow]", style="yellow")
    console.print()
    console.print(syntax)
    console.print()
