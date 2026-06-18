class RuntimeServiceGenerator:

    def generate_service(self, proposal):

        title = proposal.get("title", "service")

        service_name = (
            title.lower()
            .replace(" ", "_")
        )

        return {
            "service": service_name,
            "entrypoint": f"core/services/{service_name}.py",
            "status": "generated"
        }