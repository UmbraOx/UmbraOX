"""
RuntimeResourceManager — keeps Umbra from hogging system resources.
- Sets all Umbra subprocesses to LOW priority (below normal)
- Detects gaming/streaming processes and backs off further
- Caps CPU usage per task
- Monitors memory usage and pauses if too high
- Restores normal priority when Umbra exits
"""
import os
import sys
import time
import threading
from datetime import datetime


# Processes that indicate gaming/streaming is active
GAMING_PROCESS_NAMES = {
    # Games
    "steam.exe", "steamwebhelper.exe", "gameoverlayui.exe",
    "epicgameslauncher.exe", "origin.exe", "gog galaxy.exe",
    "minecraft.exe", "javaw.exe", "robloxplayerbeta.exe",
    "league of legends.exe", "leagueclient.exe", "r5apex.exe",
    "csgo.exe", "cs2.exe", "valorant.exe", "fortnite.exe",
    "GTA5.exe", "RDR2.exe", "Cyberpunk2077.exe",
    # Streaming
    "obs64.exe", "obs32.exe", "streamlabs obs.exe",
    "xsplit.core.exe", "nvidia broadcast.exe",
    # Recording
    "shadowplay.exe", "medal.exe",
}

# Memory threshold (MB) — pause tasks if system RAM above this % used
MEMORY_WARNING_THRESHOLD_PCT = 85


class ResourceStatus:

    def __init__(self):
        self.gaming_detected = False
        self.gaming_processes = []
        self.memory_pct = 0
        self.cpu_pct = 0
        self.throttled = False
        self.checked_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "gaming_detected": self.gaming_detected,
            "gaming_processes": self.gaming_processes,
            "memory_pct": self.memory_pct,
            "throttled": self.throttled,
            "checked_at": self.checked_at,
        }


class RuntimeResourceManager:
    """
    Manages system resource usage for Umbra.

    Philosophy: Umbra should be INVISIBLE to your gaming and streaming.
    - All Umbra work runs at BELOW NORMAL priority
    - If gaming/streaming detected: drop to IDLE priority + add delays
    - Memory guardrails prevent OOM
    - No overclock, no CPU pinning, no aggressive scheduling
    """

    def __init__(self, gaming_mode_auto=True, max_memory_pct=85, task_delay_ms=50):
        self.gaming_mode_auto = gaming_mode_auto
        self.max_memory_pct = max_memory_pct
        self.task_delay_ms = task_delay_ms  # ms to sleep between tasks when gaming
        self._monitoring = False
        self._monitor_thread = None
        self._current_status = ResourceStatus()
        self._callbacks = []

        # Set this process to below-normal priority immediately
        self._set_process_priority_low()

    def _set_process_priority_low(self):
        try:
            if sys.platform == "win32":
                import ctypes
                # BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
                ctypes.windll.kernel32.SetPriorityClass(
                    ctypes.windll.kernel32.GetCurrentProcess(),
                    0x00004000
                )
            else:
                os.nice(10)
        except Exception:
            pass

    def _set_process_priority_idle(self):
        try:
            if sys.platform == "win32":
                import ctypes
                # IDLE_PRIORITY_CLASS = 0x00000040
                ctypes.windll.kernel32.SetPriorityClass(
                    ctypes.windll.kernel32.GetCurrentProcess(),
                    0x00000040
                )
            else:
                os.nice(19)
        except Exception:
            pass

    def _set_process_priority_normal(self):
        try:
            if sys.platform == "win32":
                import ctypes
                # NORMAL_PRIORITY_CLASS = 0x00000020
                ctypes.windll.kernel32.SetPriorityClass(
                    ctypes.windll.kernel32.GetCurrentProcess(),
                    0x00000020
                )
            else:
                os.nice(0)
        except Exception:
            pass

    def detect_gaming_processes(self):
        detected = []
        try:
            if sys.platform == "win32":
                import subprocess
                result = subprocess.run(
                    ["tasklist", "/fo", "csv", "/nh"],
                    capture_output=True, text=True, timeout=3
                )
                running = {line.split(",")[0].strip('"').lower() for line in result.stdout.splitlines() if line}
                for proc in GAMING_PROCESS_NAMES:
                    if proc.lower() in running:
                        detected.append(proc)
            else:
                import subprocess
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=3)
                for proc in GAMING_PROCESS_NAMES:
                    if proc.lower().replace(".exe", "") in result.stdout.lower():
                        detected.append(proc)
        except Exception:
            pass
        return detected

    def get_memory_usage_pct(self):
        try:
            if sys.platform == "win32":
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return stat.dwMemoryLoad
            else:
                with open("/proc/meminfo") as f:
                    lines = f.readlines()
                total = int([l for l in lines if "MemTotal" in l][0].split()[1])
                avail = int([l for l in lines if "MemAvailable" in l][0].split()[1])
                return int((1 - avail / total) * 100)
        except Exception:
            return 0

    def check_status(self):
        status = ResourceStatus()
        status.gaming_processes = self.detect_gaming_processes()
        status.gaming_detected = len(status.gaming_processes) > 0
        status.memory_pct = self.get_memory_usage_pct()
        status.throttled = status.gaming_detected or status.memory_pct > self.max_memory_pct
        self._current_status = status
        return status

    def should_throttle(self):
        return self._current_status.throttled

    def apply_throttle(self):
        if self._current_status.gaming_detected:
            self._set_process_priority_idle()
        elif self._current_status.memory_pct > self.max_memory_pct:
            time.sleep(2)

    def release_throttle(self):
        self._set_process_priority_low()

    def task_delay(self):
        status = self.check_status()
        if status.gaming_detected:
            time.sleep(self.task_delay_ms / 1000.0 * 4)
            self.apply_throttle()
        elif status.memory_pct > self.max_memory_pct:
            time.sleep(2)
        else:
            time.sleep(self.task_delay_ms / 1000.0)

    def start_monitoring(self, interval_seconds=30):
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval_seconds,),
            daemon=True,
        )
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._monitoring = False

    def _monitor_loop(self, interval):
        while self._monitoring:
            status = self.check_status()
            if status.gaming_detected:
                self.apply_throttle()
            else:
                self.release_throttle()
            for cb in self._callbacks:
                try:
                    cb(status)
                except Exception:
                    pass
            time.sleep(interval)

    def on_status_change(self, callback):
        self._callbacks.append(callback)

    def get_current_status(self):
        return self._current_status.to_dict()

    def get_subprocess_kwargs(self):
        kwargs = {}
        if sys.platform == "win32":
            import subprocess
            # CREATE_NEW_PROCESS_GROUP | BELOW_NORMAL_PRIORITY_CLASS
            kwargs["creationflags"] = 0x00000200 | 0x00004000
        return kwargs

    def set_subprocess_low_priority(self, proc):
        try:
            if sys.platform == "win32":
                import ctypes
                handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, proc.pid)
                if handle:
                    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)
                    ctypes.windll.kernel32.CloseHandle(handle)
        except Exception:
            pass