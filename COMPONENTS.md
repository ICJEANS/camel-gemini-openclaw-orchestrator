# COMPONENTS

This project is intentionally componentized so parts can be removed quickly.

## Core Components

1. Router (`src/coop/router_gpt_mini.py`)
   - Selects skills/MCPs and per-domain tasks.
2. Role Assigner (`src/coop/role_assigner.py`)
   - Builds role prompts per domain.
3. Executor (`src/coop/executor.py`)
   - Runs workers and applies retry/timeout policy.
4. Retry Controller (`src/coop/retry_controller.py`)
   - Centralized retry/backoff logic.
5. Reviewer (`src/coop/reviewer.py`)
   - Summarizes worker outcomes.
6. Reporter (`src/coop/reporter.py`)
   - Writes JSONL/Markdown artifacts.
7. Config Loader (`src/coop/config.py`)
   - Pipeline settings from `configs/pipeline_config.json`.

## How to disable a component quickly
- Router bypass: hardcode plan in `coop_pipeline.py`.
- Reviewer off: skip `review_results` call.
- Reporter off: skip `persist_run` call.
- Retries off: set retries to 0.
- Worker count reduce: set `workersPerDomain` in config.
