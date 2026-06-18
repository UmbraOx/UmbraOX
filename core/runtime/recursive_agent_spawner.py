class RecursiveAgentSpawner:

    def spawn(self, roles):

        agents = []

        for index, role in enumerate(roles):

            agents.append({
                "id": f"agent_{index+1}",
                "role": role
            })

        return agents