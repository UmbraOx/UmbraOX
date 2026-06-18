class ObjectivePersistenceEngine:

    def persist(
        self,
        objectives
    ):

        return {
            "persisted": len(objectives),
            "status": "stored"
        }