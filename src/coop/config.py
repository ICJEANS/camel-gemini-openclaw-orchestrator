from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionConfig:
    domains: list[str]
    workers_per_domain: int
    mode: str
    retries: int
    timeout_seconds: int
    session_strategy: str


@dataclass
class PipelineConfig:
    version: str
    execution: ExecutionConfig
    router_model: str
    execution_backend: str
    execution_model: str
    runs_dir: str


def load_pipeline_config(path: str = "configs/pipeline_config.json") -> PipelineConfig:
    obj = json.loads(Path(path).read_text())
    ex = obj["execution"]
    return PipelineConfig(
        version=obj.get("version", "unknown"),
        execution=ExecutionConfig(
            domains=ex.get("domains", ["architecture", "implementation", "verification"]),
            workers_per_domain=int(ex.get("workersPerDomain", 3)),
            mode=ex.get("mode", "sequential"),
            retries=int(ex.get("retries", 1)),
            timeout_seconds=int(ex.get("timeoutSeconds", 30)),
            session_strategy=ex.get("sessionStrategy", "shared"),
        ),
        router_model=obj.get("router", {}).get("model", "gpt-4.1-mini"),
        execution_backend=obj.get("executionBackend", "codex-cli"),
        execution_model=obj.get("executionModel", "gpt-5-codex"),
        runs_dir=obj.get("artifacts", {}).get("runsDir", "runs"),
    )
