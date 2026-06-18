class RuntimeMultiAgentCoordinator:

    def coordinate(
        self,
        tasks
    ):
        coordinated = []

        for index, task in enumerate(tasks):
            coordinated.append({
                "agent": f"agent_{index+1}",
                "task": task,
                "status": "assigned"
            })

        return coordinated