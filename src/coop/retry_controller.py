from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


async def with_retry(fn: Callable[[], Awaitable[str]], retries: int = 1, base_delay: float = 1.0) -> str:
    last_err: Exception | None = None
    for i in range(retries + 1):
        try:
            return await fn()
        except Exception as e:  # noqa: BLE001
            last_err = e
            if i >= retries:
                break
            await asyncio.sleep(base_delay * (2**i))
    raise RuntimeError(f"retry exhausted: {last_err}")
