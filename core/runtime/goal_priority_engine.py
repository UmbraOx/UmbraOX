class GoalPriorityEngine:

    def prioritize(self, tasks):
        ordered = sorted(
            tasks,
            key=lambda x: x.get("domain") != "runtime"
        )

        return ordered