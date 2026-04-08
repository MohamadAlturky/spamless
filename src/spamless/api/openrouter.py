import itertools
import json
import os
import sys
from pathlib import Path
from typing import Iterator

import httpx
from dotenv import load_dotenv


def _env_path() -> Path:
    if getattr(sys, "frozen", False):
        # 1. Next to the exe (expected deployment location)
        beside_exe = Path(sys.executable).parent / ".env"
        if beside_exe.exists():
            return beside_exe
        # 2. Current working directory (user ran exe from another folder)
        in_cwd = Path.cwd() / ".env"
        if in_cwd.exists():
            return in_cwd
        return beside_exe  # let load_dotenv silently no-op; error comes from _KeyRotator
    return Path(__file__).parent.parent.parent.parent / ".env"


load_dotenv(_env_path())

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class _KeyRotator:
    def __init__(self) -> None:
        keys = [
            k
            for k in [
                os.getenv("OPENROUTER_API_KEY"),
                os.getenv("OPENROUTER_API_KEY2"),
                os.getenv("OPENROUTER_API_KEY3"),
            ]
            if k
        ]
        if not keys:
            raise RuntimeError("No OPENROUTER_API_KEY found in environment.")
        self._cycle = itertools.cycle(enumerate(keys, start=1))

    def next(self) -> tuple[int, str]:
        return next(self._cycle)


key_rotator = _KeyRotator()


def stream_completion(prompt: str) -> tuple[int, str, Iterator[str]]:
    """Return (key_index, model, chunk_iterator) for the given prompt."""
    key_index, api_key = key_rotator.next()
    model = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-001")

    def _chunks() -> Iterator[str]:
        with httpx.Client(timeout=60) as client:
            with client.stream(
                "POST",
                _OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                },
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line.startswith("data: ") or line == "data: [DONE]":
                        continue
                    data = json.loads(line[6:])
                    delta = data["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta

    return key_index, model, _chunks()
