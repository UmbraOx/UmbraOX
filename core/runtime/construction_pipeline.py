class ConstructionPipeline:

    def execute(self, blueprint):

        completed = []

        for module in blueprint.get("modules", []):

            completed.append({
                "module": module["title"],
                "status": "constructed"
            })

        return {
            "status": "success",
            "completed": completed
        }