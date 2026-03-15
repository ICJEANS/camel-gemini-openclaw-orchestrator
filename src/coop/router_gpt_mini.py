from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from .models import RoutePlan


def _keyword_select(goal: str, registry: dict) -> tuple[list[str], list[str]]:
    low = goal.lower()
    skills = []
    for s in registry.get("skills", []):
        if any(tag in low for tag in s.get("tags", [])):
            skills.append(s["id"])
    mcps = []
    for m in registry.get("mcps", []):
        if any(tag in low for tag in m.get("tags", [])):
            mcps.append(m["id"])

    if not skills:
        skills = ["orchestration", "code-review"]
    if not mcps:
        mcps = ["filesystem", "shell"]
    return sorted(set(skills)), sorted(set(mcps))


def build_route_plan(goal: str, registry_path: str, model: str = "gpt-4.1-mini") -> RoutePlan:
    registry = json.loads(Path(registry_path).read_text())

    # Try GPT-mini via OpenAI CLI first.
    prompt = (
        "Return strict JSON with keys: selected_skills (string[]), selected_mcps (string[]), "
        "teams (object with architecture/implementation/verification).\n"
        f"Goal: {goal}\nRegistry: {json.dumps(registry, ensure_ascii=False)}"
    )

    raw = ""
    if os.getenv("OPENAI_API_KEY"):
        try:
            cmd = [
                "openai", "api", "chat.completions.create",
                "-m", model,
                "-g", "system", "You are a strict JSON router. Output JSON only.",
                "-g", "user", prompt,
                "-t", "0"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            if res.returncode == 0 and res.stdout.strip():
                raw = res.stdout
                obj = json.loads(res.stdout)
                content = obj["choices"][0]["message"]["content"]
                plan = json.loads(content)
                return RoutePlan(
                    goal=goal,
                    selected_skills=plan.get("selected_skills", []),
                    selected_mcps=plan.get("selected_mcps", []),
                    teams=plan.get("teams", {}),
                    raw_text=content,
                )
        except Exception:
            pass

    # Deterministic fallback
    skills, mcps = _keyword_select(goal, registry)
    return RoutePlan(
        goal=goal,
        selected_skills=skills,
        selected_mcps=mcps,
        teams={
            "architecture": f"{goal}의 구조 설계와 리스크 식별",
            "implementation": f"{goal} 구현 단계와 작업 항목 정의",
            "verification": f"{goal} 검증 기준과 테스트 계획 수립",
        },
        raw_text=raw,
    )
