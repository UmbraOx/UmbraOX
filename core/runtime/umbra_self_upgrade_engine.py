class UmbraSelfUpgradeEngine:

    def upgrades(
        self,
        objective
    ):

        return [
            {
                "type": "optimization",
                "target": objective
            },
            {
                "type": "expansion",
                "target": objective
            },
            {
                "type": "stabilization",
                "target": objective
            }
        ]