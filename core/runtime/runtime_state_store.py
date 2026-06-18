from __future__ import annotations

import json
from pathlib import Path


class RuntimeStateStore:

    def __init__(
        self,
        path: str = "workspace/runtime_state.json",
    ):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():
            self.save({})

    def load(self):
        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    def save(self, data: dict):
        self.path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def update(self, key: str, value):
        data = self.load()
        data[key] = value
        self.save(data)
        return data