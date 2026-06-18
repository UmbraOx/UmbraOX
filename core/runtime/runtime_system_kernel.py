from core.runtime.runtime_event_bus import RuntimeEventBus
from core.runtime.runtime_health_monitor import RuntimeHealthMonitor
from core.runtime.runtime_diagnostics import RuntimeDiagnostics


class RuntimeSystemKernel:

    def __init__(self):
        self.bus = RuntimeEventBus()
        self.health = RuntimeHealthMonitor()
        self.diagnostics = RuntimeDiagnostics()

    def boot(self):
        return {
            "status": "online",
            "health": self.health.heartbeat(),
            "diagnostics": self.diagnostics.run_checks()
        }