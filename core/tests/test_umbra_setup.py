import pytest
import os
import sys
import json

_UMBRA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)


def test_setup_directories_creates_dirs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import importlib
    import umbra_setup
    importlib.reload(umbra_setup)
    umbra_setup._UMBRA_ROOT = str(tmp_path)
    umbra_setup.setup_directories()
    assert (tmp_path / "workspaces").exists()
    assert (tmp_path / "sessions").exists()
    assert (tmp_path / "continuations").exists()


def test_write_config_creates_file(tmp_path, monkeypatch):
    import importlib
    import umbra_setup
    importlib.reload(umbra_setup)
    umbra_setup._UMBRA_ROOT = str(tmp_path)
    umbra_setup.CONFIG_PATH = str(tmp_path / "umbra_config.json")
    config = umbra_setup.write_config("ollama", "llama3")
    assert (tmp_path / "umbra_config.json").exists()
    assert config["llm_provider"] == "ollama"
    assert config["llm_model"] == "llama3"


def test_write_config_valid_json(tmp_path):
    import umbra_setup
    umbra_setup._UMBRA_ROOT = str(tmp_path)
    umbra_setup.CONFIG_PATH = str(tmp_path / "umbra_config.json")
    umbra_setup.write_config("ollama", "qwen2.5-coder:14b")
    with open(str(tmp_path / "umbra_config.json")) as f:
        data = json.load(f)
    assert data["llm_provider"] == "ollama"
    assert data["llm_model"] == "qwen2.5-coder:14b"


def test_choose_provider_ollama_when_running():
    import umbra_setup
    result = umbra_setup.choose_provider(True)
    assert result == "ollama"


def test_choose_provider_default_when_no_llm():
    import umbra_setup
    result = umbra_setup.choose_provider(False)
    assert result == "ollama"


def test_choose_model_prefers_qwen(monkeypatch):
    import umbra_setup
    models = ["llama3:latest", "qwen2.5-coder:14b", "mistral:latest"]
    result = umbra_setup.choose_model("ollama", models)
    assert "qwen2.5-coder" in result


def test_choose_model_falls_back_to_llama3(monkeypatch):
    import umbra_setup
    models = ["llama3:latest", "mistral:latest"]
    result = umbra_setup.choose_model("ollama", models)
    assert "llama3" in result


def test_choose_model_default_when_no_models():
    import umbra_setup
    result = umbra_setup.choose_model("ollama", [])
    assert result == "llama3"


def test_verify_python_passes():
    import umbra_setup
    result = umbra_setup.verify_python()
    assert result is True