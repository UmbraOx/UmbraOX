from __future__ import annotations

from core.runtime.runtime_safety_rules import RuntimeSafetyRules


class RuntimePatchValidator:
    def __init__(self):
        self.safety_rules = RuntimeSafetyRules()

    def validate_patch(self, patch_code: str) -> bool:
        return self.safety_rules.validate_code(patch_code)