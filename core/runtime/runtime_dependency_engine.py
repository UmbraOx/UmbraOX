class RuntimeDependencyEngine:

    def __init__(
        self,
        registry,
        graph
    ):

        self.registry = registry

        self.graph = graph

    def infer_dependencies(
        self,
        module_name
    ):

        dependencies = []

        modules = self.registry.all()

        for name in modules.keys():

            if name == module_name:
                continue

            prefix = module_name.split("_")[0]

            if prefix in name:

                dependencies.append(name)

                self.graph.add_edge(
                    module_name,
                    name
                )

        return list(
            set(dependencies)
        )

    def build_dependency_map(self):

        mapping = {}

        for module in self.registry.all().keys():

            mapping[module] = (
                self.infer_dependencies(
                    module
                )
            )

        return mapping