class RuntimeBridge:

    def connect(
        self,
        source,
        target
    ):
        return {
            "source": source,
            "target": target,
            "connected": True
        }