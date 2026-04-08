# spamless

> In the AI world, this is the real AI.

---

## The Problem

Modern AI tools are verbose by design. They think out loud, hedge every answer, pad responses with summaries, and generate walls of text before getting to the point. The result is a bloated feedback loop where signal drowns in noise — and your context window fills up with filler before the actual work begins.

## What spamless does

**spamless** is an agentic CLI tool built around one principle: *less is more*.

It cuts the fat out of AI-assisted workflows by:

- **Minimizing context** — only what's needed to complete the task gets passed to the model. No bloated prompts, no redundant history.
- **Tool-first execution** — actions are driven by tools, not tokens. The model does, rather than explains.
- **Human-in-the-loop** — you stay in control at every decision point. The tool pauses, asks, and acts — it doesn't monologue.
- **Long-term memory** — a built-in database stores context that matters across sessions, so you don't have to repeat yourself and the model doesn't have to rediscover what it already knows.

## Philosophy

Most AI tools optimize for *appearing* thorough. spamless optimizes for *being* useful.

Every token has a cost — in latency, in price, and in cognitive load. spamless treats context as a resource to be managed, not a canvas to fill. The goal is the tightest possible loop between intent and outcome.

## Usage

```bash
spamless
```

You'll be prompted to describe what to filter, then choose how to handle it. That's it.

---

## Planner Mode

```bash
spamless --plan
```

Launches an interactive AI planning session in the current directory. You name a plan (or select an existing `.md` file), then iterate on it through conversation. The plan file is your persistent memory — it's the only context the AI ever sees.

### How the loop works

1. Enter a plan name (autocompleted from `.md` files in the current folder)
2. The current plan is displayed in the terminal
3. You type a message — a question, a request to add/change something, or a direction
4. The AI replies with a direct answer and, when needed, a fully updated plan
5. If the plan changed, a color-coded diff is shown (green = added, red = removed)
6. You accept or reject — acceptance saves to disk, rejection is a no-op
7. Repeat from step 2

### AI approach

The planner is built around three principles:

**1. The plan is the memory.**
No conversation history is maintained between turns. Each request sends only two things to the model: the current plan content and your message. This keeps token usage minimal and forces the plan to remain the authoritative source of truth — if it's not in the plan, it doesn't exist.

**2. Structured XML output.**
The AI always emits a `<answer>` block (its conversational reply) and optionally a `<plan>` block (the full updated plan). This separation means the answer streams live to your terminal while the plan update is parsed after streaming completes. You see the response in real time without blocking on plan parsing.

**3. Full-plan replacement, never partial patches.**
When the AI updates the plan, it emits the complete document — not a diff or a patch. This eliminates merge logic entirely. The diff you see is computed locally between the on-disk version and the AI's proposed version, so you always know exactly what would change before committing.

**Why no history?**
Conversation history inflates context costs and creates drift — the AI starts optimizing for the conversation rather than the plan. By resetting context each turn, the plan must stand on its own, which produces cleaner, more self-contained documents. Think of it as forcing good discipline: if the plan needs the chat context to make sense, the plan isn't complete yet.

## Install

```bash
pip install spamless
```

Or from source:

```bash
git clone https://github.com/mohamad-alturky/spamless
cd spamless
pip install -e .
```

## License

MIT
