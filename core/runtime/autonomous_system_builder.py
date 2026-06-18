class AutonomousSystemBuilder:

    def build(
        self,
        prompt
    ):

        return {
            "system": prompt,
            "autonomous": True
        }