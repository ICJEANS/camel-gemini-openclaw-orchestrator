from __future__ import annotations

from typing import Protocol

from .models import RoutePlan, WorkerResult


class Router(Protocol):
    def route(self, goal: str, registry_path: str, model: str) -> RoutePlan: ...


class RoleAssigner(Protocol):
    def assign(self, goal: str, skills: list[str], mcps: list[str]) -> dict[str, str]: ...


class Executor(Protocol):
    async def run_domain(self, domain: str, role_prompt: str, task: str) -> list[WorkerResult]: ...


class Reviewer(Protocol):
    def review(self, results: list[WorkerResult]) -> str: ...
