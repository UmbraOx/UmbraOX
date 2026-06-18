class AgentCoordinationEngine:

    def coordinate(self, agents):

        coordination = []

        for agent in agents:

            coordination.append({
                "agent": agent["id"],
                "status": "coordinated"
            })

        return coordination