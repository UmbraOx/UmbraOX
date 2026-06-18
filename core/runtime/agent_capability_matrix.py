class AgentCapabilityMatrix:

    def build(self, roles):

        matrix = {}

        for role in roles:

            matrix[role] = {
                "active": True,
                "tasks": [],
                "priority": 1
            }

        return matrix