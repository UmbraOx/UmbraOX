class RuntimeObjectiveGraph:

    def build(self, objective):

        return {
            "objective": objective,
            "children": [
                {
                    "id": "phase_1",
                    "objective":
                    f"{objective} :: architecture"
                },
                {
                    "id": "phase_2",
                    "objective":
                    f"{objective} :: implementation"
                },
                {
                    "id": "phase_3",
                    "objective":
                    f"{objective} :: validation"
                },
                {
                    "id": "phase_4",
                    "objective":
                    f"{objective} :: deployment"
                }
            ]
        }