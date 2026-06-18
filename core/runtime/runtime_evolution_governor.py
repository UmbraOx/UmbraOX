import time
from collections import deque
from pathlib import Path


class EvolutionGovernor:
    """
    CENTRAL SAFETY CONTROLLER FOR UMBRA EVOLUTION

    Prevents:
    - infinite self-mod loops
    - rapid repeated patching
    - core system destabilization
    """

    def __init__(
        self,
        max_patches_per_minute: int = 3,
        cooldown_seconds: int = 30
    ):
        self.max_patches = max_patches_per_minute
        self.cooldown = cooldown_seconds

        self.patch_log = deque(maxlen=50)
        self.locked = False

        self.protected_paths = [
            "core/runtime/runtime_self_evolver.py",
            "core/runtime/runtime_evolution_governor.py",
            "core/runtime/umbra_runtime_kernel.py",
        ]

    # -------------------------
    # ALLOW / DENY PATCH
    # -------------------------
    def allow_patch(self, file_path: str) -> bool:
        now = time.time()

        if self.locked:
            return False

        if any(p in file_path for p in self.protected_paths):
            return False

        self._cleanup(now)

        if len(self.patch_log) >= self.max_patches:
            return False

        self.patch_log.append(now)
        return True

    # -------------------------
    # COOLDOWN LOGIC
    # -------------------------
    def _cleanup(self, now):
        while self.patch_log and now - self.patch_log[0] > self.cooldown:
            self.patch_log.popleft()

    # -------------------------
    # EMERGENCY LOCKDOWN
    # -------------------------
    def lockdown(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def status(self):
        return {
            "locked": self.locked,
            "recent_patches": len(self.patch_log)
        }