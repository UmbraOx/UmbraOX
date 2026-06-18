import os

BASE_DIR = "C:\\Umbra"

# 🔒 STRICT SANDBOX ROOT (CRITICAL)
SANDBOX_PATH = os.path.join(BASE_DIR, "sandbox")

# Core paths
LOG_PATH = os.path.join(BASE_DIR, "logs")
WORKSPACE_PATH = os.path.join(BASE_DIR, "workspace")

# Memory system
MEMORY_PATH = os.path.join(BASE_DIR, "database", "memory.json")

# Runtime system
RUNTIME_PATH = os.path.join(BASE_DIR, "runtime")
TASKS_PATH = os.path.join(RUNTIME_PATH, "tasks")
SNAPSHOT_PATH = os.path.join(RUNTIME_PATH, "snapshots")
REGISTRY_PATH = os.path.join(RUNTIME_PATH, "registry")

# Model config
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5-coder:14b"