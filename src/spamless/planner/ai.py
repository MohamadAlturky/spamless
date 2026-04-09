from rich.console import Console
from rich.live import Live
from rich.text import Text

from spamless.api.openrouter import stream_completion_with_system
from spamless.ui.banner import _header
from spamless.ui.theme import SECONDARY_COLOR

PLANNER_SYSTEM_PROMPT = """\
You are an interactive planning assistant embedded in a developer CLI tool.

You help the user build a clear, well-scoped plan by maintaining two sections:

1. **Context** — confirmed goals, decisions, constraints, and background.
2. **Clarifications** — open questions you need the user to answer before the plan can progress.

## Output format

Always respond using this exact XML structure:

<answer>
Your conversational reply. If you have open questions, ask them here — ask the most important
one first. Never ask more than 2 questions at once. Be direct and concise.
</answer>
<context>
Everything confirmed and decided so far. Written as clear, factual statements.
Use Markdown: ## subheadings, - bullets, **bold** for key decisions.
Only include things actually known. No placeholders or assumptions.
</context>
<clarifications>
Open questions as a Markdown checklist:
- [ ] First open question?
- [ ] Second open question?

Mark answered items [x] so the user can track progress.
Omit this block entirely if there are no open questions.
</clarifications>

## Behavior rules
- **Start by asking**: When the user gives a vague request, populate <clarifications> with
  targeted questions and ask the most critical one in <answer>.
- **Never invent**: If something is unknown, put a question in <clarifications> instead of
  guessing.
- **Move to context**: When the user answers a clarification, move the confirmed information
  into <context> and mark the question [x] in <clarifications> (remove it the next turn).
- **Omit unchanged sections**: Only emit <context> if context changed. Only emit
  <clarifications> if clarifications changed.
- **Keep context scannable**: bullet points over paragraphs, facts over prose.\
"""


def _extract_tag(text: str, tag: str) -> str | None:
    """Extract content between <tag> and </tag>. Returns None if tag absent."""
    open_tag = f"<{tag}>"
    close_tag = f"</{tag}>"
    start = text.find(open_tag)
    if start == -1:
        return None
    start += len(open_tag)
    end = text.find(close_tag, start)
    if end == -1:
        result = text[start:].strip()
        return result or None
    return text[start:end].strip()


def stream_plan_response(
    context: str,
    clarifications: str,
    user_message: str,
    console: Console,
) -> tuple[str, str | None, str | None]:
    """
    Stream AI response for a planning turn.
    Renders the <answer> portion live.
    Returns (answer_text, new_context_or_None, new_clarifications_or_None).
    """
    ctx_text = context.strip() or "(empty — nothing confirmed yet)"
    clar_text = clarifications.strip() or "(none)"
    user_content = (
        f"Current context:\n---\n{ctx_text}\n---\n\n"
        f"Current clarifications:\n---\n{clar_text}\n---\n\n"
        f"User message: {user_message}"
    )
    messages = [{"role": "user", "content": user_content}]

    _key_index, _model, chunks = stream_completion_with_system(
        PLANNER_SYSTEM_PROMPT, messages
    )

    full_response = ""
    live_text = ""
    answer_started = False
    answer_ended = False
    answer_open = "<answer>"
    answer_close = "</answer>"

    console.print()
    _header(console, "Answer", "cyan")
    console.print()

    with Live(Text(""), console=console, refresh_per_second=15) as live:
        for chunk in chunks:
            full_response += chunk

            if not answer_started:
                idx = full_response.find(answer_open)
                if idx != -1:
                    answer_started = True
                    after_open = full_response[idx + len(answer_open):]
                    close_idx = after_open.find(answer_close)
                    if close_idx != -1:
                        live_text = after_open[:close_idx].strip()
                        answer_ended = True
                    else:
                        live_text = after_open.strip()
                    live.update(Text(live_text))
            elif not answer_ended:
                idx = full_response.find(answer_open)
                after_open = full_response[idx + len(answer_open):]
                close_idx = after_open.find(answer_close)
                if close_idx != -1:
                    live_text = after_open[:close_idx].strip()
                    answer_ended = True
                else:
                    live_text = after_open.strip()
                live.update(Text(live_text))

    console.print()

    answer = _extract_tag(full_response, "answer") or full_response.strip()
    new_context = _extract_tag(full_response, "context")
    new_clarifications = _extract_tag(full_response, "clarifications")
    return answer, new_context, new_clarifications
