class ServiceScaffolder:

    def scaffold(self, proposal):

        title = proposal.get(
            "title",
            "service"
        )

        return {
            "service_name": (
                title.lower()
                .replace(" ", "_")
            ),
            "status": "scaffolded"
        }