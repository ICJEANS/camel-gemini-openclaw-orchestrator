from src.coop.config import load_pipeline_config


def test_load_pipeline_config():
    cfg = load_pipeline_config("configs/pipeline_config.json")
    assert cfg.version == "2.0.0"
    assert cfg.execution.workers_per_domain == 3
    assert "architecture" in cfg.execution.domains
