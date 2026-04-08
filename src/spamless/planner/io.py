from pathlib import Path


def _parse_sections(content: str) -> tuple[str, str]:
    """Split markdown into (context, clarifications) by ## headings."""
    context = ""
    clarifications = ""

    ctx_marker = "## Context"
    clar_marker = "## Clarifications"

    ctx_pos = content.find(ctx_marker)
    clar_pos = content.find(clar_marker)

    if ctx_pos != -1:
        ctx_body_start = ctx_pos + len(ctx_marker)
        ctx_end = clar_pos if (clar_pos != -1 and clar_pos > ctx_pos) else len(content)
        context = content[ctx_body_start:ctx_end].strip()

    if clar_pos != -1:
        clar_body_start = clar_pos + len(clar_marker)
        clarifications = content[clar_body_start:].strip()

    return context, clarifications


def _build_markdown(context: str, clarifications: str) -> str:
    """Combine context and clarifications back into a markdown document."""
    md = f"## Context\n\n{context.strip() or '_Nothing confirmed yet._'}"
    if clarifications.strip():
        md += f"\n\n## Clarifications\n\n{clarifications.strip()}"
    return md


def load_plan(path: Path) -> tuple[str, str]:
    """Read plan file. Returns (context, clarifications); both empty if file missing."""
    if not path.exists():
        return "", ""
    content = path.read_text(encoding="utf-8")
    return _parse_sections(content)


def save_plan(path: Path, context: str, clarifications: str) -> None:
    """Write context + clarifications to disk as a structured markdown file."""
    md = _build_markdown(context, clarifications)
    path.write_text(md.replace("\r\n", "\n"), encoding="utf-8")
