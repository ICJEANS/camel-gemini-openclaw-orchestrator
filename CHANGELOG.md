# CHANGELOG

## v3.1.0
- Switched default execution backend to Codex CLI (`executionBackend=codex-cli`).
- Added `src/codex_cli_bridge.py` and tests.
- Kept GPT CLI bridge as optional fallback backend.
- Updated pipeline config/docs/changelog for Codex-first flow.

## v3.0.0
- Switched execution backend from OpenClaw delegation to GPT CLI bridge.
- Added `src/gpt_cli_bridge.py` for worker task execution.
- Updated coop pipeline/docs to GPT CLI-first architecture.
- Added `tests/test_gpt_cli_bridge.py`.

## v2.0.0
- Added full coop pipeline orchestration with required features 1~7:
  - GPT-mini router
  - skill/MCP selection registry
  - role assignment
  - OpenClaw execution orchestration
  - CAMEL-style reviewer summary
  - retry/backoff controller
  - artifact reporter (JSONL + Markdown)
- Added componentization docs (`COMPONENTS.md`).
- Added pipeline config file (`configs/pipeline_config.json`) and config loader.

## v1.1.0 ~ v1.9.0 (rolled into v2.0.0)
- Incremental internal refactors completed during integration:
  - timeout propagation to bridge
  - executor worker count configurability
  - CLI config/model/retry overrides
  - stable default sequential execution policy
