class RuntimeAPIGateway:

    def execute(
        self,
        endpoint,
        payload=None
    ):

        return {
            "endpoint": endpoint,
            "payload": payload,
            "status": "success"
        }