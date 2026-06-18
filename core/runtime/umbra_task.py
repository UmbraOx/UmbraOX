from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class UmbraTask:
    """
    Canonical task object used across entire system.
    """

    id: str
    goal: str
    status: str = "pending"

    created_at: float = field(default_factory=time.time)

    # decomposition
    steps: List[str] = field(default_factory=list)
    current_step: int = 0

    # execution
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    # metadata
    context: Dict[str, Any] = field(default_factory=dict)

    def is_complete(self):
        return self.status == "completed"

    def next_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.current_step += 1
            return step
        return None