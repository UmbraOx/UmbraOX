from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time


@dataclass
class UmbraTask:
    """
    Unified task object for ALL systems:
    image, sprite, game, audio, video, patch, etc.
    """

    task_type: str
    prompt: str
    priority: int = 5

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: float = field(default_factory=lambda: time.time())

    status: str = "queued"

    result: Optional[Dict[str, Any]] = None