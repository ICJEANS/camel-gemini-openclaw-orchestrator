from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path


class CodexCliBridge:
    """Executes worker tasks via Codex CLI non-interactive mode."""

    def __init__(self, model: str = "gpt-5-codex", dry_run: bool = True, workspace: str = "."):
        self.model = model
        self.dry_run = dry_run
        self.workspace = workspace

    async def execute(self, task: str, timeout_seconds: int = 60) -> str:
        if self.dry_run:
            await asyncio.sleep(0.05)
            return f"DRY_RUN: {task[:160]}"

        with tempfile.NamedTemporaryFile(prefix="codex-last-", suffix=".txt", delete=False) as tf:
            out_path = Path(tf.name)

        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--full-auto",
            "--cd",
            self.workspace,
            "-m",
            self.model,
            "--output-last-message",
            str(out_path),
            task,
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
            raise RuntimeError(f"codex-cli timeout after {timeout_seconds}s")

        if proc.returncode != 0:
            raise RuntimeError((stderr.decode() or stdout.decode()).strip() or "codex-cli failed")

        if out_path.exists():
            text = out_path.read_text(encoding="utf-8", errors="ignore").strip()
            try:
                out_path.unlink(missing_ok=True)
            except Exception:
                pass
            if text:
                return text

        return stdout.decode().strip() or "(empty)"
