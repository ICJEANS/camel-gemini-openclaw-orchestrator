from __future__ import annotations

import argparse
import asyncio
import uuid

from src.coop.config import load_pipeline_config
from src.coop.executor import CoopExecutor
from src.coop.models import RunArtifacts
from src.coop.reporter import persist_run
from src.coop.reviewer import review_results
from src.coop.role_assigner import build_roles
from src.coop.router_gpt_mini import build_route_plan
from src.gpt_cli_bridge import GPTCliBridge


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GPT-mini router + GPT CLI execution + CAMEL review pipeline")
    p.add_argument("goal", help="Top-level user goal")
    p.add_argument("--registry", default="configs/skills_registry.json")
    p.add_argument("--config", default="configs/pipeline_config.json")
    p.add_argument("--model", default=None, help="Override router model")
    p.add_argument("--live", action="store_true")
    p.add_argument("--retries", type=int, default=None, help="Override retries")
    return p.parse_args()


async def _run(args: argparse.Namespace) -> None:
    cfg = load_pipeline_config(args.config)
    model = args.model or cfg.router_model
    retries = cfg.execution.retries if args.retries is None else args.retries

    plan = build_route_plan(args.goal, args.registry, model=model)
    roles = build_roles(args.goal, plan.selected_skills, plan.selected_mcps)

    bridge = GPTCliBridge(model=model, dry_run=not args.live)
    executor = CoopExecutor(
        bridge=bridge,
        retries=retries,
        workers_per_domain=cfg.execution.workers_per_domain,
        timeout_seconds=cfg.execution.timeout_seconds,
    )

    all_results = []
    for domain in cfg.execution.domains:
        task = plan.teams.get(domain, f"{args.goal} ({domain})")
        all_results.extend(await executor.run_domain(domain, roles[domain], task))

    review = review_results(all_results)
    art = RunArtifacts(
        run_id=uuid.uuid4().hex[:10],
        goal=args.goal,
        plan=plan,
        results=all_results,
        review=review,
        meta={"model": model, "live": args.live, "pipeline_version": cfg.version},
    )
    jsonl_path, md_path = persist_run(art, runs_dir=cfg.runs_dir)

    print(f"[Pipeline v{cfg.version}]")
    print(review)
    print(f"\nArtifacts:\n- {jsonl_path}\n- {md_path}")


def main() -> None:
    args = parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
