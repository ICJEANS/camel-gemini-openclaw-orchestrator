from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Any


@dataclass
class GeminiChiefPlanner:
    """
    Uses Gemini API for planning/summarization when GEMINI_API_KEY exists.
    Falls back to deterministic local templates otherwise.
    """

    model: str = "gemini-2.5-pro"

    async def make_plan(self, goal: str, domains: Iterable[str]) -> Dict[str, str]:
        domains = list(domains)
        if os.getenv("GEMINI_API_KEY"):
            text = self._gemini_call(
                f"Create one concise execution task per domain for this goal: {goal}\n"
                f"Domains: {', '.join(domains)}\n"
                "Return JSON object: {domain: task}."
            )
            parsed = self._safe_parse_json(text, domains)
            if parsed:
                return parsed

        return {d: f"{goal} ({d} 관점에서 실행)" for d in domains}

    async def summarize(self, goal: str, plan: Dict[str, str], team_runs: List[Any]) -> str:
        joined_runs = "\n\n".join(str(x) for x in team_runs)
        if os.getenv("GEMINI_API_KEY"):
            text = self._gemini_call(
                "Summarize this multi-team execution result briefly in Korean.\n"
                f"Goal: {goal}\nPlan: {plan}\nResults:\n{joined_runs}"
            )
            if text:
                return text.strip()

        return (
            f"[Gemini Chief Fallback Summary]\n"
            f"목표: {goal}\n"
            f"도메인 계획: {plan}\n\n"
            f"팀 결과:\n{joined_runs}"
        )

    def _gemini_call(self, prompt: str) -> str:
        # Lazy import so project can run without dependency in fallback mode.
        from google import genai  # type: ignore

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        response = client.models.generate_content(model=self.model, contents=prompt)
        return (response.text or "").strip()

    def _safe_parse_json(self, text: str, domains: List[str]) -> Dict[str, str] | None:
        import json

        try:
            obj = json.loads(text)
            if not isinstance(obj, dict):
                return None
            out: Dict[str, str] = {}
            for d in domains:
                v = obj.get(d)
                if isinstance(v, str) and v.strip():
                    out[d] = v.strip()
            return out if len(out) == len(domains) else None
        except Exception:
            return None
