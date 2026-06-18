class RuntimeFailoverManager:

    def __init__(self):

        self.failovers = []

    def failover(
        self,
        target
    ):

        self.failovers.append(target)

        return {
            "status": "failover_started",
            "target": target
        }