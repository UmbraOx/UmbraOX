from core.runtime.runtime_paths import RuntimePaths
from core.runtime.runtime_logger import RuntimeLogger
from core.runtime.runtime_state import RuntimeState
from core.runtime.runtime_registry import RuntimeRegistry
from core.runtime.runtime_event_bus import RuntimeEventBus
from core.runtime.runtime_config import RuntimeConfig


class RuntimeBootloader:

    def boot(self):

        RuntimePaths.ensure()

        logger = RuntimeLogger()

        logger.log(
            "BOOT",
            "Initializing Umbra Runtime"
        )

        state = RuntimeState()

        registry = RuntimeRegistry()

        event_bus = RuntimeEventBus()

        config = RuntimeConfig()

        state.set(
            "runtime_booted",
            True
        )

        logger.log(
            "BOOT",
            "Umbra Runtime Online"
        )

        return {
            "state": state,
            "registry": registry,
            "event_bus": event_bus,
            "config": config
        }