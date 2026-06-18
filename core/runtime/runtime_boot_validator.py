class RuntimeBootValidator:
    """
    VALIDATES SYSTEM INTEGRITY BEFORE START

    Prevents partial/fragmented runtime launches
    """

    def __init__(self, registry):
        self.registry = registry

    def validate(self):
        issues = []

        if not self.registry.active_kernel:
            issues.append("No active kernel registered")

        if len(self.registry.components) == 0:
            issues.append("No runtime components registered")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }