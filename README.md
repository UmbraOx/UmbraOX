# UMBRA — Autonomous AI Runtime OS

**Runtime Core v2** | Python 3.12 | Ollama (local, free) | 500+ tests

Umbra is a fully autonomous, recursive, self-improving multi-agent AI production platform. Give it an objective, it decomposes it into tasks, generates Python code, validates it, writes files to disk, and tracks everything.

## Quick Start

```powershell
# 1. First-time setup
python umbra_setup.py

# 2. Start interactive mode
python umbra.py

# 3. Or run a single task
python umbra.py "write a Python script that monitors disk usage"
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `status` | Runtime status, model, session info |
| `health` | System health check (Ollama, dirs, Python) |
| `analyze` | Self-analyze codebase for gaps |
| `metrics` | Pipeline execution metrics |
| `memory` | Show memory store contents |
| `history` | Run history for this session |
| `resume` | Resume failed/partial runs |
| `handoff` | Generate session handoff document |
| `remember <fact>` | Store a fact in memory |
| `recall <query>` | Search memory |
| `help` | Show config and provider options |
| `exit` | Quit Umbra |

## LLM Configuration (All Free)

### Ollama (local, unlimited, recommended)
```powershell
# Install from https://ollama.com
ollama pull qwen2.5-coder:14b   # Best for code
ollama pull llama3               # General purpose
$env:UMBRA_LLM_MODEL = "qwen2.5-coder:14b"
python umbra.py
```

### Groq (free cloud, fast)
```powershell
# Get free key at https://console.groq.com
$env:UMBRA_LLM_PROVIDER = "groq"
$env:UMBRA_LLM_API_KEY = "gsk_YOUR_KEY"
python umbra.py
```

## Architecture
umbra.py (CLI entry point)
└─ build_runtime() assembles:
├─ RuntimeLLMProvider       -- Ollama/Groq/OpenAI/Anthropic
├─ RuntimeConfigManager     -- Central config with env overrides
├─ RuntimeExecutionGraph    -- DAG-based task dependencies
├─ RuntimeTaskStateMachine  -- Task lifecycle management
├─ RuntimeContextBuilder    -- LLM context assembly
├─ RuntimeValidationEngine  -- Python syntax + schema validation
├─ RuntimeRecursionGuard    -- Depth/call protection
├─ RuntimeWorkspaceManager  -- Project isolation
├─ RuntimeLLMOrchestrator   -- Wires LLM + graph + state
├─ RuntimeAutonomousPipeline-- Main prompt-to-code loop
├─ RuntimeCodeExtractor     -- Extract Python from LLM responses
├─ RuntimeCodeWriter        -- Write validated Python to disk
├─ RuntimeCodeRunner        -- Execute generated Python
├─ RuntimePipelineMonitor   -- Track metrics across runs
├─ RuntimeMemoryStore       -- Persistent key-value memory
├─ RuntimeHealthMonitor     -- System health checks
├─ RuntimeSessionManager    -- Cross-session persistence
├─ RuntimeTaskContinuation  -- Resume incomplete runs
└─ RuntimeSelfAnalyzer      -- Codebase gap detection

## Running Tests

```powershell
python -m pytest core/tests -v --timeout=30
```

## Project Structure
C:\Umbra
umbra.py              # CLI entry point
umbra_setup.py        # First-run wizard
umbra_config.json     # Auto-generated config
core/runtime/         # 60+ runtime modules
core/tests/           # 500+ tests
workspaces/           # Generated code outputs
sessions/             # Session data + memory
continuations/        # Incomplete run saves
snapshots/            # State snapshots

## Generated Code

Every run creates a workspace directory:
workspaces/run_0001/
task_plan.json         # Decomposed tasks
graph_summary.json     # Execution graph state
written_files.json     # List of code files written
code/
run_0001_task_1.py   # Generated Python files
run_0001_task_2.py
run_0001_task_3.py
results/
run_0001_task_1.json # Task execution results

## Self-Improvement

Umbra can analyze its own codebase and generate improvements:
umbra> analyze
[SELF-ANALYSIS]
Modules      : 60
With tests   : 55
Missing tests: 5
Improvement targets: ...

---
Built with Python 3.12 | Powered by Ollama + qwen2.5-coder:14b