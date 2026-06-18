from core.runtime.runtime_self_repair_engine_v2 import RuntimeSelfRepairEngineV2


class RuntimeSelfRepairEngine:
    """
    Legacy wrapper (keeps compatibility)
    """

    def __init__(self, root_dir: str):
        self.engine = RuntimeSelfRepairEngineV2(root_dir)

    def scan(self):
        return self.engine.scan()

    def export_report(self):
        return self.engine.export_report()