# core/runtime/resource_guardian.py

class ResourceGuardian:
    def __init__(self, cpu_cap=70, ram_cap=75):
        self.cpu_cap = cpu_cap
        self.ram_cap = ram_cap
        self.gpu_cap = 70  # placeholder for future GPU integration

    def can_execute_heavy_task(self, system_stats):
        cpu_ok = system_stats["cpu"] < self.cpu_cap
        ram_ok = system_stats["ram"] < self.ram_cap
        return cpu_ok and ram_ok

    def throttle_level(self, system_stats):
        cpu = system_stats["cpu"]

        if cpu > self.cpu_cap:
            return "HIGH_THROTTLE"
        elif cpu > self.cpu_cap * 0.7:
            return "MEDIUM_THROTTLE"
        return "NORMAL"