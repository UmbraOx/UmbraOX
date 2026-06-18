# core/runtime/system_monitor.py

import psutil
import time
import threading

class SystemMonitor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.cpu = 0
        self.ram = 0
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            self.cpu = psutil.cpu_percent(interval=None)
            self.ram = psutil.virtual_memory().percent
            time.sleep(self.interval)

    def get_stats(self):
        return {
            "cpu": self.cpu,
            "ram": self.ram
        }