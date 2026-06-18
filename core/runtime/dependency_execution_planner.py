class DependencyExecutionPlanner:

    def build_plan(
        self,
        objectives
    ):

        plan = []

        previous = None

        for objective in objectives:

            node = {
                "objective": objective,
                "depends_on": previous
            }

            plan.append(node)

            previous = objective

        return plan