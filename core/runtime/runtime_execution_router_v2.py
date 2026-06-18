class RuntimeExecutionRouterV2:

    def route(
        self,
        objective
    ):
        lowered = objective.lower()

        if "gui" in lowered:
            return "ui"

        if "memory" in lowered:
            return "memory"

        if "agent" in lowered:
            return "agents"

        return "runtime"