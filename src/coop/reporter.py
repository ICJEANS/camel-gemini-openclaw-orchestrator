from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import RunArtifacts


def persist_run(art: RunArtifacts, runs_dir: str = "runs") -> tuple[str, str]:
    run_path = Path(runs_dir) / art.run_id
    run_path.mkdir(parents=True, exist_ok=True)

    jsonl_path = run_path / "results.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in art.results:
            f.write(json.dumps(r.__dict__, ensure_ascii=False) + "\n")

    md_path = run_path / "report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# Run Report: {art.run_id}\n\n")
        f.write(f"- goal: {art.goal}\n")
        f.write(f"- created: {datetime.now().isoformat()}\n")
        f.write(f"- skills: {', '.join(art.plan.selected_skills)}\n")
        f.write(f"- mcps: {', '.join(art.plan.selected_mcps)}\n\n")
        f.write("## Review\n")
        f.write(art.review + "\n\n")
        f.write("## Worker Results\n")
        for r in art.results:
            f.write(f"- [{r.domain}] {r.worker} ({r.status})\n")

    return str(jsonl_path), str(md_path)
