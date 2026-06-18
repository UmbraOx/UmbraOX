from pathlib import Path


class RuntimeModuleIdentity:
    """
    Canonical module identity system.

    Prevents:
    - full path leakage
    - duplicate module references
    - analyzer instability
    """

    def normalize(self, module_path: str) -> str:
        if not module_path:
            return "unknown"

        p = str(module_path)

        # extract filename without extension
        name = Path(p).stem

        # strip obvious runtime noise
        name = name.replace("\\", "/").split("/")[-1]

        return name

    def batch_normalize(self, modules):
        return [self.normalize(m) for m in modules if m]