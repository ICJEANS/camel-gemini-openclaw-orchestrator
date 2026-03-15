import asyncio

from src.codex_cli_bridge import CodexCliBridge


def test_codex_cli_bridge_dry_run():
    bridge = CodexCliBridge(model="gpt-5-codex", dry_run=True)
    out = asyncio.run(bridge.execute("hello", timeout_seconds=1))
    assert out.startswith("DRY_RUN:")
