from __future__ import annotations

import asyncio
import os
from typing import List


class OpenClawBridge:
    """Thin async bridge that delegates execution tasks to OpenClaw CLI agent turns."""

    def __init__(self, session_key: str | None = None, dry_run: bool = True):
        self.session_key = session_key
        self.dry_run = dry_run

    @staticmethod
    def _resolve_target_args(session_key: str | None) -> List[str]:
        """Build OpenClaw targeting args from a session key.

        Priority:
        1) UUID-like session id -> --session-id
        2) session-key format "agent:<id>:..." -> --agent <id>
        3) fallback -> --agent main
        """
        if session_key:
            # UUID-like explicit session id
            if "-" in session_key and session_key.count("-") >= 4:
                return ["--session-id", session_key]

            # OpenClaw session-key style: agent:<agentId>:...
            parts = session_key.split(":")
            if len(parts) >= 2 and parts[0] == "agent" and parts[1]:
                return ["--agent", parts[1]]

        return ["--agent", "main"]

    def _build_cmd(self, task: str) -> List[str]:
        return [
            "openclaw",
            "agent",
            *self._resolve_target_args(self.session_key),
            "--message",
            task,
            "--timeout",
            "30",
        ]

    async def execute(self, task: str) -> str:
        if self.dry_run:
            await asyncio.sleep(0.05)
            return f"DRY_RUN: {task[:120]}"

        cmd = self._build_cmd(task)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(stderr.decode().strip() or "openclaw agent failed")
        return stdout.decode().strip() or "(empty)"
