class AgentTaskBridge:

    def bridge(
        self,
        agent,
        task
    ):

        return {
            "agent": agent,
            "task": task,
            "bridge": "connected"
        }