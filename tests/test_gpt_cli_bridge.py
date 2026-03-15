import asyncio

from src.gpt_cli_bridge import GPTCliBridge


def test_gpt_cli_bridge_dry_run():
    bridge = GPTCliBridge(model="gpt-4.1-mini", dry_run=True)
    out = asyncio.run(bridge.execute("hello", timeout_seconds=1))
    assert out.startswith("DRY_RUN:")
