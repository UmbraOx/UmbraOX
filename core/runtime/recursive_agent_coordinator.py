class RecursiveAgentCoordinator:

    def coordinate(self, objectives):
        workers = []

        for index, objective in enumerate(objectives, start=1):
            workers.append({
                "agent": f"agent_{index}",
                "objective": objective,
                "status": "assigned"
            })

        return workers