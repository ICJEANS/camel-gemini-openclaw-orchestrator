from __future__ import annotations


def build_roles(goal: str, skills: list[str], mcps: list[str]) -> dict[str, str]:
    common = (
        f"Goal: {goal}\n"
        f"Enabled skills: {', '.join(skills)}\n"
        f"Enabled MCPs: {', '.join(mcps)}\n"
        "Return concise, actionable output."
    )
    return {
        "architecture": "You are architecture lead. Focus on decomposition, constraints, interfaces.\n" + common,
        "implementation": "You are implementation lead. Focus on concrete tasks, code changes, command steps.\n" + common,
        "verification": "You are verification lead. Focus on tests, edge cases, acceptance criteria.\n" + common,
    }
