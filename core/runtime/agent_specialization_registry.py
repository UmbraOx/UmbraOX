class AgentSpecializationRegistry:

    def __init__(self):
        self.specializations = {
            "builder": ["generate", "construct"],
            "planner": ["plan", "analyze"],
            "reviewer": ["verify", "inspect"],
            "deployer": ["deploy", "release"]
        }

    def get(self, role):
        return self.specializations.get(role, [])