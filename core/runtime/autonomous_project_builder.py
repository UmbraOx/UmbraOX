class AutonomousProjectBuilder:

    def build(self, blueprint):

        generated = []

        for module in blueprint.get("modules", []):

            generated.append({
                "module": module["title"],
                "target": module["target"],
                "status": "prepared"
            })

        return {
            "status": "ready",
            "generated": generated
        }