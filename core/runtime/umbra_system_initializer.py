from core.runtime.runtime_daemon_loop import (
    RuntimeDaemonLoop
)


class UmbraSystemInitializer:

    def initialize(self):
        daemon = RuntimeDaemonLoop()

        daemon.start()

        return {
            "umbra": "initialized"
        }