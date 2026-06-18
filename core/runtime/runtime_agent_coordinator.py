from core.runtime.runtime_task_router import (
    RuntimeTaskRouter
)


class RuntimeAgentCoordinator:

    def __init__(
        self,
        registry
    ):

        self.registry = registry

        self.router = (
            RuntimeTaskRouter()
        )

    def delegate(
        self,
        task
    ):

        target = (
            self.router.route(
                task
            )
        )

        agent = (
            self.registry.get_agent(
                target
            )
        )

        if not agent:

            return {
                "success": False,
                "error": "agent_not_found",
                "target": target
            }

        return {
            "success": True,
            "task": task,
            "assigned_to": target
        }