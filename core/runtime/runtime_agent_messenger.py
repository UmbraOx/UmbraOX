class RuntimeAgentMessenger:

    def send(
        self,
        sender,
        target,
        message
    ):

        return {
            "from": sender,
            "to": target,
            "message": message,
            "delivered": True
        }