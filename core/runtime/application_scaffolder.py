class ApplicationScaffolder:

    def scaffold(
        self,
        app_name
    ):

        return {
            "name": app_name,
            "type": "desktop_application",
            "modules": [
                "runtime",
                "gui",
                "agents",
                "services"
            ]
        }