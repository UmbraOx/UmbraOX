import psutil
import time


class UmbraActivityMonitor:
    """
    Detects system usage state to prevent Umbra from interfering
    with user activity (gaming, streaming, heavy workloads).
    """

    def __init__(self):
        self.last_state = "idle"

    def detect(self):
        cpu = psutil.cpu_percent(interval=0.3)
        mem = psutil.virtual_memory().percent

        # Detect heavy system usage
        heavy = cpu > 75 or mem > 80

        # Detect likely interactive workload via process load
        process_names = []
        try:
            for p in psutil.process_iter(['name']):
                if p.info['name']:
                    process_names.append(p.info['name'].lower())
        except Exception:
            pass

        gaming_signals = [
            "steam", "game", "elden", "valorant", "fortnite",
            "cod", "minecraft", "unity", "unreal", "obs"
        ]

        active_user_app = any(
            any(sig in name for sig in gaming_signals)
            for name in process_names
        )

        if heavy or active_user_app:
            state = "user_active_heavy"
        elif cpu < 25 and mem < 45:
            state = "idle"
        else:
            state = "normal"

        self.last_state = state
        return state