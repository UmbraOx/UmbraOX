class RuntimeApplicationBuilder:

    def build(
        self,
        application_name
    ):

        return {
            "application": application_name,
            "status": "built"
        }