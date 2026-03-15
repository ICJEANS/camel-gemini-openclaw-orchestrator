from __future__ import annotations

from collections import Counter

from .models import WorkerResult


def review_results(results: list[WorkerResult]) -> str:
    c = Counter(r.status for r in results)
    lines = [
        "[CAMEL Reviewer Summary]",
        f"- total workers: {len(results)}",
        f"- ok: {c.get('ok', 0)}",
        f"- error: {c.get('error', 0)}",
    ]
    if c.get("error", 0):
        lines.append("- action: retry failed workers or reduce tool scope")
    else:
        lines.append("- action: proceed to final reporting")
    return "\n".join(lines)
