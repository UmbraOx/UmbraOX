class ConstructionGovernor:

    def validate(self, execution_batch):

        return {
            "safe": True,
            "validated": True,
            "reason": "construction approved"
        }