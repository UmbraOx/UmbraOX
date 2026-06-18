class RuntimeAutonomousDecisionEngine:

    def decide(
        self,
        options
    ):
        if not options:
            return None

        return options[0]