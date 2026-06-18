class UIGenerationEngine:

    def generate(self, proposal):

        return {
            "window": proposal.get(
                "title",
                "Umbra Window"
            ),
            "layout": "dashboard",
            "status": "planned"
        }