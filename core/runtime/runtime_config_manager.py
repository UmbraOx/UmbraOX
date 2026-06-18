import os
import json
from datetime import datetime


class RuntimeConfigManager:
    """
    Centralized configuration management for Umbra.
    - Load/save config from JSON
    - Environment variable overrides
    - Defaults for all settings
    - Validates config values
    """

    DEFAULTS = {
        "llm_provider": "ollama",
        "llm_model": "llama3",
        "llm_api_key": "",
        "max_recursion_depth": 10,
        "max_calls_per_task": 50,
        "max_total_calls": 500,
        "subprocess_timeout": 30,
        "workspace_dir": "workspaces",
        "sessions_dir": "sessions",
        "continuations_dir": "continuations",
        "snapshots_dir": "snapshots",
        "auto_run_tests": False,
        "auto_commit_to_git": False,
        "max_tasks_per_run": 6,
        "code_runner_timeout": 15,
        "log_level": "INFO",
    }

    ENV_MAP = {
        "llm_provider": "UMBRA_LLM_PROVIDER",
        "llm_model": "UMBRA_LLM_MODEL",
        "llm_api_key": "UMBRA_LLM_API_KEY",
        "log_level": "UMBRA_LOG_LEVEL",
    }

    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(os.getcwd(), "umbra_config.json")
        self.config = dict(self.DEFAULTS)
        self._load()
        self._apply_env_overrides()

    def get(self, key, default=None):
        return self.config.get(key, default if default is not None else self.DEFAULTS.get(key))

    def set(self, key, value):
        self.config[key] = value

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def reset_to_defaults(self):
        self.config = dict(self.DEFAULTS)
        self._apply_env_overrides()

    def validate(self):
        errors = []
        if self.get("max_recursion_depth") < 1:
            errors.append("max_recursion_depth must be >= 1")
        if self.get("subprocess_timeout") < 1:
            errors.append("subprocess_timeout must be >= 1")
        if self.get("llm_provider") not in ("ollama", "groq", "openai", "anthropic"):
            errors.append(f"Unknown llm_provider: {self.get('llm_provider')}")
        return errors

    def to_dict(self):
        return dict(self.config)

    def _load(self):
        if not os.path.exists(self.config_path):
            return
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.config.update(loaded)
        except Exception:
            pass

    def _apply_env_overrides(self):
        for config_key, env_key in self.ENV_MAP.items():
            val = os.environ.get(env_key, "")
            if val:
                self.config[config_key] = val