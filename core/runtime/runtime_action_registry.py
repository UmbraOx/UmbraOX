from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class RuntimeAction:
    name: str
    description: str
    handler: Callable


class RuntimeActionRegistry:

    def __init__(self):
        self.actions = {}

    def register(
        self,
        name: str,
        description: str,
        handler,
    ):
        self.actions[name] = RuntimeAction(
            name=name,
            description=description,
            handler=handler,
        )

    def execute(
        self,
        name: str,
        payload: dict,
    ):
        if name not in self.actions:
            raise ValueError(
                f"Unknown action: {name}"
            )

        return self.actions[name].handler(payload)

    def list_actions(self):
        return {
            key: value.description
            for key, value in self.actions.items()
        }