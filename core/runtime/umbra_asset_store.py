import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from core.runtime.umbra_asset import UmbraAsset


class UmbraAssetStore:
    """
    Persistent disk-backed storage for all Umbra outputs.
    """

    def __init__(self, base_path: str = "C:\\Umbra\\assets"):

        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # SAVE
    # -------------------------

    def save(self, asset: UmbraAsset) -> UmbraAsset:

        folder = self.base_path / asset.asset_type
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{asset.asset_id}.json"

        payload = asset.to_dict()

        file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        asset.file_path = str(file_path)

        return asset

    # -------------------------
    # LOAD
    # -------------------------

    def load(self, asset_type: str, asset_id: str) -> Optional[Dict[str, Any]]:

        file_path = self.base_path / asset_type / f"{asset_id}.json"

        if not file_path.exists():
            return None

        return json.loads(file_path.read_text(encoding="utf-8"))

    # -------------------------
    # LIST
    # -------------------------

    def list_assets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:

        results = []

        base = self.base_path if asset_type is None else self.base_path / asset_type

        if not base.exists():
            return []

        for file in base.glob("*.json"):
            try:
                results.append(json.loads(file.read_text(encoding="utf-8")))
            except Exception:
                continue

        return results