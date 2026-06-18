class FeatureProposer:

    def propose(self, insight: str):
        """
        Converts system observations into structured upgrade ideas.
        """

        return {
            "idea": insight,
            "type": "system_improvement",
            "priority": "low"
        }


feature_proposer = FeatureProposer()