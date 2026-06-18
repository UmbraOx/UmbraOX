class RuntimeExpansionPlanner:

    def plan(self, proposal):

        title = proposal.get("title", "Runtime Upgrade")
        target = proposal.get("target", "core/runtime")

        return {
            "title": title,
            "target": target,
            "stages": [
                "Analysis",
                "Blueprinting",
                "Code Generation",
                "Validation",
                "Deployment"
            ]
        }