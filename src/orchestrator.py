from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import List

from .openclaw_bridge import OpenClawBridge
from .planner import GeminiChiefPlanner


@dataclass
class Worker:
    name: str
    domain: str

    async def run(self, task: str, bridge: OpenClawBridge) -> str:
        scoped_task = f"[{self.domain}/{self.name}] {task}"
        return await bridge.execute(scoped_task)


@dataclass
class TeamLead:
    name: str
    domain: str
    workers: List[Worker] = field(default_factory=list)

    async def run_team(self, task: str, bridge: OpenClawBridge) -> str:
        # Run workers sequentially to avoid OpenClaw session lock/contention.
        results = []
        for worker in self.workers:
            try:
                results.append(await worker.run(task, bridge))
            except Exception as e:
                results.append(e)

        lines = [f"팀장 {self.name} ({self.domain}) 결과:"]
        for idx, result in enumerate(results, start=1):
            if isinstance(result, Exception):
                lines.append(f"- worker{idx}: ERROR {result}")
            else:
                lines.append(f"- worker{idx}: {result}")
        return "\n".join(lines)


@dataclass
class GeminiChief:
    name: str
    planner: GeminiChiefPlanner

    async def orchestrate(self, goal: str, leads: List[TeamLead], bridge: OpenClawBridge) -> str:
        plan = await self.planner.make_plan(goal, [lead.domain for lead in leads])

        # Run leads sequentially as well for stability with shared OpenClaw runtime.
        team_runs = []
        for lead in leads:
            try:
                team_runs.append(await lead.run_team(plan[lead.domain], bridge))
            except Exception as e:
                team_runs.append(e)

        return await self.planner.summarize(goal, plan, team_runs)


@dataclass
class ThreeThreeThreeSystem:
    """
    3 domains × (3 workers + 1 team lead), then 1 Gemini chief supervisor.
    """

    chief: GeminiChief
    leads: List[TeamLead]
    bridge: OpenClawBridge

    @classmethod
    def default(cls, bridge: OpenClawBridge, planner: GeminiChiefPlanner) -> "ThreeThreeThreeSystem":
        domains = ["architecture", "implementation", "verification"]
        leads: List[TeamLead] = []
        for d_idx, domain in enumerate(domains, start=1):
            workers = [
                Worker(name=f"{domain}-ai-{i}", domain=domain)
                for i in range(1, 4)
            ]
            leads.append(TeamLead(name=f"lead-{d_idx}", domain=domain, workers=workers))

        chief = GeminiChief(name="gemini-chief", planner=planner)
        return cls(chief=chief, leads=leads, bridge=bridge)

    async def run(self, goal: str) -> str:
        return await self.chief.orchestrate(goal, self.leads, self.bridge)
