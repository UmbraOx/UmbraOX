class UmbraAgentMesh:

    def __init__(self):
        self.agents = [
            {
                "name": "architect",
                "status": "idle"
            },
            {
                "name": "coder",
                "status": "idle"
            },
            {
                "name": "reviewer",
                "status": "idle"
            },
            {
                "name": "planner",
                "status": "idle"
            },
            {
                "name": "optimizer",
                "status": "idle"
            }
        ]

    def all(self):
        return self.agents