from typing import List, Dict


class RuntimeGapAnalyzer:

    def __init__(self):

        self.required_capabilities = [
            "agent_orchestration",
            "persistent_memory",
            "safe_execution",
            "task_planning",
            "self_validation",
            "runtime_expansion"
        ]

    def analyze(
        self,
        current_capabilities: List[str] | None = None
    ) -> Dict:

        if current_capabilities is None:
            current_capabilities = []

        missing = [
            capability
            for capability in self.required_capabilities
            if capability not in current_capabilities
        ]

        complete = len(missing) == 0

        summary = {
            "required": len(self.required_capabilities),
            "current": len(current_capabilities),
            "missing": len(missing),
            "complete": complete
        }

        return {
            "summary": summary,
            "required": self.required_capabilities,
            "current": current_capabilities,
            "missing": missing,
            "priority_missing": missing,
            "complete": complete
        }