from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time
import uuid


@dataclass
class UmbraAsset:
    """
    Unified representation of ANY generated output in Umbra:
    - images
    - sprites
    - audio
    - video
    - game artifacts
    - structured outputs
    """

    asset_type: str
    data: Any

    metadata: Dict[str, Any] = field(default_factory=dict)

    asset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=lambda: time.time())

    file_path: Optional[str] = None

    status: str = "generated"

    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "data": str(self.data),
            "metadata": self.metadata,
            "created_at": self.created_at,
            "file_path": self.file_path,
            "status": self.status
        }