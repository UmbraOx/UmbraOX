from __future__ import annotations


class RuntimeSelfBuilder:
    def __init__(self):
        self.generated_capabilities: list[str] = []

    def build_missing_capability(self, capability: str) -> dict:
        self.generated_capabilities.append(capability)

        return {
            "capability": capability,
            "status": "generated",
            "success": True,
        }