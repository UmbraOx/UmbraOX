class RuntimeDependencyGraph:

    def __init__(self):

        self.dependencies = {}

    def add_dependency(
        self,
        module,
        dependency
    ):

        if module not in self.dependencies:

            self.dependencies[module] = []

        if dependency not in self.dependencies[module]:

            self.dependencies[module].append(
                dependency
            )

    def infer_dependencies(
        self,
        goal
    ):

        goal_lower = goal.lower()

        inferred = []

        keyword_map = {
            "agent": "agent_core",
            "memory": "memory_core",
            "validation": "validation_core",
            "execution": "execution_core",
            "planning": "planning_core",
            "tool": "tooling_core",
            "graph": "graph_core",
            "runtime": "runtime_core",
            "deployment": "deployment_core",
            "ui": "ui_module"
        }

        for keyword, dependency in keyword_map.items():

            if keyword in goal_lower:

                inferred.append(
                    dependency
                )

                self.add_dependency(
                    goal,
                    dependency
                )

        return inferred

    def build_dependency_map(self):

        return self.dependencies

    def clear(self):

        self.dependencies = {}