class RuntimeDependencyValidator:
    def __init__(self):
        self.required = set()

    def add_dependency(self, dependency):
        self.required.add(dependency)

    def validate(self, installed):
        missing = []

        for dep in self.required:
            if dep not in installed:
                missing.append(dep)

        return {
            "valid": len(missing) == 0,
            "missing": missing,
        }