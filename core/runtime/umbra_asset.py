from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time
import uuid


@dataclass
class UmbraAsset:
    """
    Unified output object for EVERYTHING Umbra generates:
    - images
    - sprites
    - games
    - audio
    - video
    - UI artifacts
    """

    asset_type: str
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

    asset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=lambda: time.time())

    file_path: Optional[str] = None

    status: str = "generated"