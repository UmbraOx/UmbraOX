class RuntimeDecisionRouter:

    def route_decision(
        self,
        decision
    ):

        return {
            "status": "decision_routed",
            "decision": decision
        }