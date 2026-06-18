from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RuntimeTask:
    task_id: str
    objective: str
    stage: str = "pending"
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    dependencies: List[str] = field(default_factory=list)


@dataclass
class RuntimeRun:
    run_id: str
    objective: str
    tasks: List[RuntimeTask] = field(default_factory=list)

    status: str = "running"

    written_files: List[str] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)

    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimePipelineStage:
    name: str
    objective: str
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None


@dataclass
class RuntimeExecutionContext:
    run: RuntimeRun
    current_stage: str = "init"
    metadata: Dict[str, Any] = field(default_factory=dict)