from __future__ import annotations

from core.runtime.runtime_prompt_orchestrator import RuntimePromptOrchestrator


class RuntimeSelfExtensionController:

    def __init__(self):
        self.orchestrator = (
            RuntimePromptOrchestrator()
        )

    def extend(
        self,
        objective: str,
        approved: bool = False,
    ):

        if not approved:
            return {
                "success": False,
                "reason": "human approval required",
            }

        return self.orchestrator.execute(
            objective
        )