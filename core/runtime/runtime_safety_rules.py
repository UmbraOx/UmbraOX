from __future__ import annotations


class RuntimeCapabilityExpander:
    def __init__(self):
        self.capabilities: set[str] = set()

    def register_capability(self, capability: str):
        self.capabilities.add(capability)

    def expand_capabilities(self, capabilities: list[str]):
        for capability in capabilities:
            self.register_capability(capability)

    def get_capabilities(self):
        return sorted(self.capabilities)