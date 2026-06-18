class RuntimeExecutionRouter:

    def route(self, objective):

        lowered = objective.lower()

        routes = []

        if "gui" in lowered:
            routes.append("ui")

        if "agent" in lowered:
            routes.append("agents")

        if "memory" in lowered:
            routes.append("memory")

        if "deploy" in lowered:
            routes.append("deployment")

        if (
            "runtime" in lowered
            or not routes
        ):
            routes.append("runtime")

        return list(set(routes))