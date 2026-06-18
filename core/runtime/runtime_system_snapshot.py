class RuntimeSystemSnapshot:

    def snapshot(
        self,
        runtime
    ):
        return {
            "objective": runtime.get(
                "objective"
            ),
            "status": runtime.get(
                "status"
            )
        }