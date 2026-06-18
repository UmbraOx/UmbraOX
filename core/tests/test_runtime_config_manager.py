import pytest
import os
from core.runtime.runtime_config_manager import RuntimeConfigManager


@pytest.fixture
def config(tmp_path):
    return RuntimeConfigManager(config_path=str(tmp_path / "config.json"))


def test_default_provider(config):
    assert config.get("llm_provider") == "ollama"


def test_default_model(config):
    assert config.get("llm_model") == "llama3"


def test_get_unknown_key_returns_none(config):
    assert config.get("nonexistent_key") is None


def test_get_with_fallback(config):
    assert config.get("nonexistent_key", "fallback") == "fallback"


def test_set_value(config):
    config.set("llm_provider", "groq")
    assert config.get("llm_provider") == "groq"


def test_save_and_reload(tmp_path):
    path = str(tmp_path / "cfg.json")
    c1 = RuntimeConfigManager(config_path=path)
    c1.set("llm_model", "qwen2.5-coder:14b")
    c1.save()
    c2 = RuntimeConfigManager(config_path=path)
    assert c2.get("llm_model") == "qwen2.5-coder:14b"


def test_reset_to_defaults(config):
    config.set("llm_provider", "openai")
    config.reset_to_defaults()
    assert config.get("llm_provider") == "ollama"


def test_validate_passes_with_defaults(config):
    errors = config.validate()
    assert isinstance(errors, list)
    assert len(errors) == 0


def test_validate_catches_bad_provider(config):
    config.set("llm_provider", "unknown_provider")
    errors = config.validate()
    assert len(errors) > 0


def test_validate_catches_bad_timeout(config):
    config.set("subprocess_timeout", 0)
    errors = config.validate()
    assert len(errors) > 0


def test_to_dict(config):
    d = config.to_dict()
    assert "llm_provider" in d
    assert "max_recursion_depth" in d


def test_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("UMBRA_LLM_PROVIDER", "groq")
    config = RuntimeConfigManager(config_path=str(tmp_path / "env_cfg.json"))
    assert config.get("llm_provider") == "groq"


def test_defaults_are_complete(config):
    for key in RuntimeConfigManager.DEFAULTS:
        assert config.get(key) is not None