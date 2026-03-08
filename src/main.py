from __future__ import annotations

import argparse
import asyncio

from .openclaw_bridge import OpenClawBridge
from .orchestrator import ThreeThreeThreeSystem
from .planner import GeminiChiefPlanner


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="3-3-3 CAMEL+OpenClaw hybrid orchestrator")
    p.add_argument("goal", help="Top-level goal for Gemini chief")
    p.add_argument("--session-key", default=None, help="OpenClaw target session key")
    p.add_argument("--live", action="store_true", help="Use real OpenClaw agent calls")
    p.add_argument("--model", default="gemini-2.5-pro", help="Gemini model name")
    return p


async def _run(args: argparse.Namespace) -> None:
    session_key = args.session_key
    if not session_key:
        import os
        session_key = os.getenv("OPENCLAW_SESSION_KEY")

    bridge = OpenClawBridge(session_key=session_key, dry_run=not args.live)
    planner = GeminiChiefPlanner(model=args.model)
    system = ThreeThreeThreeSystem.default(bridge=bridge, planner=planner)
    output = await system.run(args.goal)
    print(output)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
