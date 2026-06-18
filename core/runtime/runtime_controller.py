from core.runtime.runtime_bootloader import (
    RuntimeBootloader
)

from core.runtime.unified_runtime_engine import (
    UnifiedRuntimeEngine
)


class RuntimeController:

    def __init__(self):

        self.bootloader = RuntimeBootloader()

        self.runtime = self.bootloader.boot()

        self.engine = UnifiedRuntimeEngine()

    def execute(self, objective):

        return self.engine.execute(
            objective
        )