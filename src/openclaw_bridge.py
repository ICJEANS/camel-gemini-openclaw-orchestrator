from __future__ import annotations

import asyncio
import os
import shlex


class OpenClawBridge:
    """Thin async bridge that delegates execution tasks to OpenClaw CLI agent turns."""

    def __init__(self, session_key: str | None = None, dry_run: bool = True):
        self.session_key = session_key
        self.dry_run = dry_run

    async def execute(self, task: str) -> str:
        if self.dry_run:
            await asyncio.sleep(0.05)
            return f"DRY_RUN: {task[:120]}"

        # Delegate to OpenClaw agent in non-interactive mode.
        # Keep this minimal/safe; caller controls task scope.
        quoted = shlex.quote(task)
        cmd = f"openclaw agent --message {quoted} --timeout 30"
        # OpenClaw CLI supports --session-id (not --session-key).
        # If caller passes a UUID-like value, use it; otherwise run in default session routing.
        if self.session_key and "-" in self.session_key and self.session_key.count("-") >= 4:
            cmd += f" --session-id {shlex.quote(self.session_key)}"

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(stderr.decode().strip() or "openclaw agent failed")
        return stdout.decode().strip() or "(empty)"
