class GuiRuntimeManager:

    def create_dashboard(self):

        return {
            "window": "Umbra Control Center",
            "panels": [
                "agents",
                "runtime",
                "tasks",
                "deployments",
                "governance"
            ]
        }