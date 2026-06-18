class MultiAgentTopology:

    def build(self):

        return {
            "boss_agent": "orchestrator",
            "coder_agent": "implementation",
            "reviewer_agent": "validation",
            "architect_agent": "planning",
            "repair_agent": "self_repair",
            "ui_agent": "desktop_generation"
        }