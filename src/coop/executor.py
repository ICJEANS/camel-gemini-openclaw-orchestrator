from __future__ import annotations

from dataclasses import dataclass

from .models import WorkerResult
from .retry_controller import with_retry
from ..openclaw_bridge import OpenClawBridge


@dataclass
class CoopExecutor:
    bridge: OpenClawBridge
    retries: int = 1
    workers_per_domain: int = 3
    timeout_seconds: int = 30

    async def run_domain(self, domain: str, role_prompt: str, task: str) -> list[WorkerResult]:
        results: list[WorkerResult] = []
        for idx in range(1, self.workers_per_domain + 1):
            worker = f"{domain}-ai-{idx}"

            async def _call() -> str:
                return await self.bridge.execute(
                    f"[{worker}] {role_prompt}\nTask: {task}",
                    timeout_seconds=self.timeout_seconds,
                )

            try:
                out = await with_retry(_call, retries=self.retries, base_delay=1.0)
                results.append(WorkerResult(worker=worker, domain=domain, status="ok", output=out))
            except Exception as e:  # noqa: BLE001
                results.append(WorkerResult(worker=worker, domain=domain, status="error", output=str(e)))
        return results
