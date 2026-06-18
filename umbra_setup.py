"""
UMBRA Setup Wizard
Run this once to configure your Umbra installation.
Usage: python umbra_setup.py
"""

import os
import sys
import json
import urllib.request

_UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_UMBRA_ROOT, "umbra_config.json")

REQUIRED_DIRS = [
    "workspaces", "sessions", "continuations",
    "snapshots", "core/runtime", "core/tests",
]


def check_ollama():
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            return True, models
    except Exception:
        return False, []


def print_header():
    print("\n" + "=" * 60)
    print("  UMBRA — First Run Setup Wizard")
    print("=" * 60)


def setup_directories():
    print("\n[1/5] Creating directories...")
    for d in REQUIRED_DIRS:
        path = os.path.join(_UMBRA_ROOT, d)
        os.makedirs(path, exist_ok=True)
        print(f"  + {d}")
    print("  Done.")


def detect_llm():
    print("\n[2/5] Detecting LLM providers...")
    ollama_running, models = check_ollama()

    if ollama_running:
        print(f"  + Ollama is running!")
        if models:
            print(f"    Available models: {', '.join(models[:5])}")
            if any("qwen2.5-coder" in m for m in models):
                print("    Recommended: qwen2.5-coder:14b (already installed!)")
            elif any("llama3" in m or "llama" in m for m in models):
                print("    Recommended: llama3 (already installed!)")
        else:
            print("    No models found. Run: ollama pull llama3")
        return "ollama", models
    else:
        print("  ! Ollama not running (install from https://ollama.com)")
        print("  ! Groq free tier available at https://console.groq.com")
        return None, []


def choose_provider(ollama_running):
    print("\n[3/5] Choosing provider...")
    if ollama_running:
        print("  Using Ollama (free, local) as default provider.")
        return "ollama"
    else:
        print("  No local LLM detected.")
        print("  Options:")
        print("    1. Install Ollama: https://ollama.com (recommended)")
        print("    2. Use Groq free tier: https://console.groq.com")
        print("  Defaulting to ollama (configure later with 'python umbra.py --config')")
        return "ollama"


def choose_model(provider, available_models):
    print("\n[4/5] Selecting model...")
    if provider == "ollama" and available_models:
        preferred = ["qwen2.5-coder:14b", "qwen2.5-coder:7b", "llama3", "llama3.2", "llama2"]
        for p in preferred:
            if any(p in m for m in available_models):
                match = next(m for m in available_models if p in m)
                print(f"  Selected: {match}")
                return match
        model = available_models[0]
        print(f"  Selected: {model} (first available)")
        return model
    else:
        print("  Using default: llama3")
        return "llama3"


def write_config(provider, model):
    print("\n[5/5] Writing config...")
    config = {
        "llm_provider": provider,
        "llm_model": model,
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
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"  Config saved to: {CONFIG_PATH}")
    return config


def verify_python():
    major, minor = sys.version_info[:2]
    if major == 3 and minor >= 10:
        print(f"  Python {major}.{minor} -- OK")
        return True
    elif major == 3 and minor >= 8:
        print(f"  Python {major}.{minor} -- OK (3.10+ recommended)")
        return True
    else:
        print(f"  Python {major}.{minor} -- UNSUPPORTED. Need 3.8+")
        return False


def main():
    print_header()
    print("\nThis wizard configures Umbra for first use.")

    if not verify_python():
        sys.exit(1)

    setup_directories()

    ollama_running, available_models = detect_llm()
    provider = choose_provider(ollama_running)
    model = choose_model(provider, available_models)
    config = write_config(provider, model)

    print("\n" + "=" * 60)
    print("  UMBRA SETUP COMPLETE")
    print("=" * 60)
    print(f"\n  Provider : {config['llm_provider']}")
    print(f"  Model    : {config['llm_model']}")
    print(f"\n  Start Umbra:  python umbra.py")
    print(f"  Run tests:    python -m pytest core/tests -v --timeout=30")
    print(f"  Check health: python umbra.py --health")
    print()

    if not ollama_running:
        print("  NEXT STEPS:")
        print("  1. Install Ollama from https://ollama.com")
        print("  2. Run: ollama pull qwen2.5-coder:14b")
        print("  3. Run: python umbra.py")
        print()


if __name__ == "__main__":
    main()