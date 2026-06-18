class RuntimeSelfRebuilder:

    def rebuild(
        self,
        objective
    ):
        return {
            "objective": objective,
            "rebuilt": True
        }