class RuntimeAgentSupervisor:

    def __init__(self):

        self.active_agents = []

    def supervise(
        self,
        agents
    ):

        self.active_agents = agents

        return {
            "status": "supervising",
            "agents": agents
        }