import pytest

from ceradon_sam_bot.config import ConfigError, load_config


def test_config_validation_missing_keys(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("filters: {}\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(config_path)
