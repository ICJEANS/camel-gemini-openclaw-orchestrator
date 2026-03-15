from __future__ import annotations

import asyncio
import json
import os


class GPTCliBridge:
    """Executes worker tasks via OpenAI CLI (chat.completions.create)."""

    def __init__(self, model: str = "gpt-4.1-mini", dry_run: bool = True):
        self.model = model
        self.dry_run = dry_run

    async def execute(self, task: str, timeout_seconds: int = 30) -> str:
        if self.dry_run:
            await asyncio.sleep(0.05)
            return f"DRY_RUN: {task[:160]}"

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is missing")

        cmd = [
            "openai",
            "api",
            "chat.completions.create",
            "-m",
            self.model,
            "-g",
            "system",
            "You are a coding copilot worker. Return concise actionable output.",
            "-g",
            "user",
            task,
            "-t",
            "0",
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
        )

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_seconds)
        except TimeoutError:
            proc.kill()
            raise RuntimeError(f"gpt-cli timeout after {timeout_seconds}s")

        if proc.returncode != 0:
            raise RuntimeError(stderr.decode().strip() or "gpt-cli failed")

        raw = stdout.decode().strip()
        try:
            obj = json.loads(raw)
            return obj["choices"][0]["message"]["content"].strip()
        except Exception:
            # Fallback: return raw if JSON shape differs.
            return raw or "(empty)"
