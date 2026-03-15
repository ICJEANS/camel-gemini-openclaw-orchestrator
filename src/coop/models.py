from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RoutePlan:
    goal: str
    selected_skills: list[str]
    selected_mcps: list[str]
    teams: dict[str, str]
    raw_text: str = ""


@dataclass
class WorkerResult:
    worker: str
    domain: str
    status: str
    output: str


@dataclass
class RunArtifacts:
    run_id: str
    goal: str
    plan: RoutePlan
    results: list[WorkerResult] = field(default_factory=list)
    review: str = ""
    meta: dict[str, Any] = field(default_factory=dict)
