from pathlib import Path


class RuntimeModuleRegistry:

    def __init__(self):

        self.modules = []

    def discover_generated_modules(self):

        runtime_path = Path(
            "core/runtime"
        )

        discovered = []

        if not runtime_path.exists():

            return []

        for file in runtime_path.glob("*.py"):

            if file.name.startswith("__"):

                continue

            module_name = file.stem

            discovered.append(
                module_name
            )

        self.modules = sorted(
            list(set(discovered))
        )

        return self.modules

    def get_modules(self):

        return self.modules