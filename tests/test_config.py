from src.coop.config import load_pipeline_config


def test_load_pipeline_config():
    cfg = load_pipeline_config("configs/pipeline_config.json")
    assert cfg.version == "3.1.0"
    assert cfg.execution.workers_per_domain == 3
    assert cfg.execution_backend == "codex-cli"
    assert cfg.execution_model == "gpt-5-codex"
    assert "architecture" in cfg.execution.domains
