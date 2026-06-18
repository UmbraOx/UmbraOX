from datetime import UTC
from datetime import datetime


class RuntimeCapabilityPlanner:

    def __init__(self):

        self.templates = {
            "execution": [
                "validate_request",
                "allocate_resources",
                "execute_task",
                "verify_output"
            ],
            "generation": [
                "analyze_goal",
                "build_plan",
                "generate_code",
                "validate_generation"
            ],
            "improvement": [
                "scan_runtime",
                "detect_weakness",
                "build_patch",
                "verify_patch"
            ]
        }

    def build_plan(
        self,
        capability_type,
        objective
    ):

        steps = self.templates.get(
            capability_type,
            []
        )

        return {
            "objective": objective,
            "capability_type": capability_type,
            "steps": steps,
            "created": (
                datetime.now(UTC).isoformat()
            )
        }