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
