import psutil
import time


class SystemMonitor:
    """
    Lightweight system telemetry collector.
    """

    def snapshot(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "time": time.time()
        }