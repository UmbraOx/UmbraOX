class AgentRuntimeBuilder:

    def build_agent_runtime(
        self,
        name
    ):

        return {
            "agent": name,
            "runtime_ready": True,
            "channels": [
                "tasks",
                "memory",
                "events"
            ]
        }