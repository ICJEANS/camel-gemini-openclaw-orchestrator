from __future__ import annotations

import argparse
import asyncio
import os
import uuid

from src.coop.executor import CoopExecutor
from src.coop.models import RunArtifacts
from src.coop.reporter import persist_run
from src.coop.reviewer import review_results
from src.coop.role_assigner import build_roles
from src.coop.router_gpt_mini import build_route_plan
from src.openclaw_bridge import OpenClawBridge


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GPT-mini router + OpenClaw execution + CAMEL review pipeline")
    p.add_argument("goal", help="Top-level user goal")
    p.add_argument("--registry", default="configs/skills_registry.json")
    p.add_argument("--model", default="gpt-4.1-mini")
    p.add_argument("--live", action="store_true")
    p.add_argument("--session-key", default=None)
    p.add_argument("--retries", type=int, default=1)
    return p.parse_args()


async def _run(args: argparse.Namespace) -> None:
    plan = build_route_plan(args.goal, args.registry, model=args.model)
    roles = build_roles(args.goal, plan.selected_skills, plan.selected_mcps)

    session_key = args.session_key or os.getenv("OPENCLAW_SESSION_KEY")
    bridge = OpenClawBridge(session_key=session_key, dry_run=not args.live)
    executor = CoopExecutor(bridge=bridge, retries=args.retries)

    all_results = []
    for domain in ("architecture", "implementation", "verification"):
        task = plan.teams.get(domain, f"{args.goal} ({domain})")
        all_results.extend(await executor.run_domain(domain, roles[domain], task))

    review = review_results(all_results)
    art = RunArtifacts(
        run_id=uuid.uuid4().hex[:10],
        goal=args.goal,
        plan=plan,
        results=all_results,
        review=review,
        meta={"model": args.model, "live": args.live},
    )
    jsonl_path, md_path = persist_run(art)

    print(review)
    print(f"\nArtifacts:\n- {jsonl_path}\n- {md_path}")


def main() -> None:
    args = parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
