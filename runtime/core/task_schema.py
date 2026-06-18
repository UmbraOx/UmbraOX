from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Task:
    id: str
    goal: str
    status: str = "pending"
    subtasks: List[Dict[str, Any]] = field(default_factory=list)
    assigned_agent: str = "boss"
    metadata: Dict[str, Any] = field(default_factory=dict)