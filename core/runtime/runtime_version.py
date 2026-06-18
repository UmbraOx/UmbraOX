"""
UMBRA Version Information
"""

VERSION = "2.0.0"
VERSION_NAME = "Runtime Core v2"
BUILD_DATE = "2026-05-26"
CODENAME = "Autonomous"

CHANGELOG = {
    "2.0.0": [
        "Full autonomous pipeline: prompt -> plan -> code -> execute -> validate",
        "500+ tests covering all runtime modules",
        "Self-analysis and self-improvement loop",
        "Persistent memory store with search",
        "Pipeline metrics and monitoring",
        "Health monitoring system",
        "Git integration for auto-committing generated code",
        "Smart prompt templates for better code quality",
        "Run validation with scoring",
        "Code review engine",
        "Session replay for regression testing",
        "Resource manager: gaming/streaming priority protection",
        "Setup wizard with Ollama auto-detection",
        "Multi-provider LLM support: Ollama, Groq, OpenAI, Anthropic",
        "Task continuation for resuming failed runs",
        "Priority task queue",
        "Agent pool for parallel execution",
        "Full CLI with 15+ commands",
        "README and requirements.txt",
    ]
}


def get_version():
    return VERSION


def get_full_version():
    return f"UMBRA v{VERSION} ({VERSION_NAME}) — {CODENAME}"


def print_version():
    print(f"\n{get_full_version()}")
    print(f"Build date: {BUILD_DATE}")
    print(f"Modules: core/runtime/ (60+ modules)")
    print(f"Tests: core/tests/ (500+ tests)")
    print()