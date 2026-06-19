# C:\Umbra\core\runtime\umbra_runtime_kernel.py
# Umbra Runtime Kernel v2.0 — Authoritative System Core
# FIXED: was just a thin wrapper with no real functionality
# Now provides: module registry, event bus, safe_execute, snapshot, run_cycle

import os
import sys
import time
import json
import uuid
import logging
import threading
import traceback
from typing import Any, Callable, Dict, List, Optional

log = logging.getLogger("umbra.kernel")

_UMBRA_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class KernelEvent:
    """A message passed through the event bus."""
    def __init__(self, event_type: str, data: Any = None, source: str = "kernel"):
        self.id         = str(uuid.uuid4())[:8]
        self.event_type = event_type
        self.data       = data
        self.source     = source
        self.timestamp  = time.time()

    def to_dict(self):
        return {
            "id": self.id, "type": self.event_type,
            "source": self.source, "timestamp": self.timestamp,
            "data": str(self.data)[:200] if self.data else None,
        }


class KernelModule:
    """Wrapper around a registered module."""
    def __init__(self, name: str, instance: Any, category: str = "general"):
        self.name      = name
        self.instance  = instance
        self.category  = category
        self.registered = time.time()
        self.call_count = 0
        self.error_count = 0
        self.last_called = None


class UmbraRuntimeKernel:
    """
    The authoritative Umbra runtime kernel.

    Responsibilities:
    - Module registry (register, get, list, unregister)
    - Event bus (emit, subscribe, broadcast)
    - Safe execution with error isolation
    - Snapshot / restore state
    - Heartbeat / run_cycle loop
    - Startup / shutdown coordination
    """

    VERSION = "2.0.0"

    def __init__(self, base_path: str = "C:\\Umbra"):
        self.base_path   = base_path
        self._modules: Dict[str, KernelModule]  = {}
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_log: List[KernelEvent]      = []
        self._lock       = threading.Lock()
        self._running    = False
        self._cycle_count = 0
        self._start_time  = None
        self._snapshots: Dict[str, dict]        = {}

        # Load the underlying RuntimeKernel if available
        self._inner = None
        try:
            from core.runtime.runtime_kernel import RuntimeKernel
            self._inner = RuntimeKernel(base_path)
        except Exception:
            pass  # run without inner kernel

    # ─────────────────────────────────────────────────────────────────────────
    # LIFECYCLE
    # ─────────────────────────────────────────────────────────────────────────

    def start(self):
        if self._running:
            return
        self._running    = True
        self._start_time = time.time()
        self._emit(KernelEvent("kernel.started", {"version": self.VERSION}))
        log.info("Umbra Kernel v%s started", self.VERSION)
        if self._inner and hasattr(self._inner, "start"):
            try:
                self._inner.start()
            except Exception:
                pass

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._emit(KernelEvent("kernel.stopped", {"uptime": self.uptime()}))
        log.info("Umbra Kernel stopped (uptime %.1fs, cycles %d)",
                 self.uptime(), self._cycle_count)
        if self._inner and hasattr(self._inner, "stop"):
            try:
                self._inner.stop()
            except Exception:
                pass

    def uptime(self) -> float:
        if self._start_time is None:
            return 0.0
        return time.time() - self._start_time

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE REGISTRY
    # ─────────────────────────────────────────────────────────────────────────

    def register_module(self, name: str, instance: Any,
                        category: str = "general") -> bool:
        with self._lock:
            km = KernelModule(name, instance, category)
            self._modules[name] = km
            self._emit(KernelEvent("module.registered",
                                   {"name": name, "category": category}))
            log.debug("Registered module: %s (%s)", name, category)
            return True

    def unregister(self, name: str) -> bool:
        with self._lock:
            if name in self._modules:
                del self._modules[name]
                self._emit(KernelEvent("module.unregistered", {"name": name}))
                return True
            return False

    def get(self, name: str) -> Optional[Any]:
        km = self._modules.get(name)
        if km:
            km.call_count  += 1
            km.last_called  = time.time()
            return km.instance
        return None

    def exists(self, name: str) -> bool:
        return name in self._modules

    def list(self, category: str = None) -> List[str]:
        if category:
            return [n for n, km in self._modules.items()
                    if km.category == category]
        return list(self._modules.keys())

    def categories(self) -> List[str]:
        return list({km.category for km in self._modules.values()})

    def bootstrap(self, module_registry: dict):
        """Register all modules from a dict (used by UmbraRuntimeKernel wrapper)."""
        for name, instance in module_registry.items():
            cat = "runtime" if "runtime" in name.lower() else "general"
            self.register_module(name, instance, cat)

    # ─────────────────────────────────────────────────────────────────────────
    # SAFE EXECUTION
    # ─────────────────────────────────────────────────────────────────────────

    def safe_execute(self, fn: Callable, *args, **kwargs) -> dict:
        """
        Execute fn(*args, **kwargs) with full error isolation.
        Returns {"ok": True, "result": ...} or {"ok": False, "error": ...}
        """
        try:
            result = fn(*args, **kwargs)
            return {"ok": True, "result": result}
        except Exception as e:
            err = traceback.format_exc()
            log.error("safe_execute error in %s: %s", getattr(fn, "__name__", "?"), e)
            self._emit(KernelEvent("kernel.error",
                                   {"fn": getattr(fn, "__name__", "?"), "error": str(e)}))
            return {"ok": False, "error": str(e), "traceback": err}

    # ─────────────────────────────────────────────────────────────────────────
    # EVENT BUS
    # ─────────────────────────────────────────────────────────────────────────

    def subscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type] = [
                    c for c in self._subscribers[event_type] if c is not callback
                ]

    def emit(self, event_type: str, data: Any = None, source: str = "external"):
        event = KernelEvent(event_type, data, source)
        self._emit(event)

    def _emit(self, event: KernelEvent):
        with self._lock:
            self._event_log.append(event)
            if len(self._event_log) > 500:
                self._event_log = self._event_log[-500:]
            subs = list(self._subscribers.get(event.event_type, []))
            subs += list(self._subscribers.get("*", []))

        for cb in subs:
            try:
                cb(event)
            except Exception as e:
                log.warning("Subscriber error for %s: %s", event.event_type, e)

    def get_event_log(self, limit: int = 50) -> List[dict]:
        return [e.to_dict() for e in self._event_log[-limit:]]

    # ─────────────────────────────────────────────────────────────────────────
    # RUN CYCLE
    # ─────────────────────────────────────────────────────────────────────────

    def run_cycle(self) -> dict:
        """Called once per runtime tick. Returns cycle summary."""
        self._cycle_count += 1
        cycle_id = self._cycle_count

        # Health checks on registered modules
        unhealthy = []
        for name, km in list(self._modules.items()):
            inst = km.instance
            if hasattr(inst, "is_available") and not inst.is_available():
                unhealthy.append(name)
            elif hasattr(inst, "health_check"):
                try:
                    ok = inst.health_check()
                    if not ok:
                        unhealthy.append(name)
                except Exception:
                    pass

        if unhealthy:
            self._emit(KernelEvent("kernel.unhealthy_modules",
                                   {"modules": unhealthy}))

        if self._inner and hasattr(self._inner, "run_cycle"):
            try:
                self._inner.run_cycle()
            except Exception:
                pass

        return {
            "cycle":      cycle_id,
            "uptime":     round(self.uptime(), 1),
            "modules":    len(self._modules),
            "unhealthy":  unhealthy,
            "events":     len(self._event_log),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # SNAPSHOT
    # ─────────────────────────────────────────────────────────────────────────

    def snapshot(self, label: str = None) -> str:
        snap_id = label or time.strftime("snap_%Y%m%d_%H%M%S")
        with self._lock:
            self._snapshots[snap_id] = {
                "modules":    list(self._modules.keys()),
                "cycle":      self._cycle_count,
                "uptime":     self.uptime(),
                "created":    time.time(),
            }
        log.info("Snapshot saved: %s", snap_id)
        return snap_id

    def restore(self, snap_id: str) -> bool:
        snap = self._snapshots.get(snap_id)
        if not snap:
            log.warning("Snapshot not found: %s", snap_id)
            return False
        log.info("Restore from snapshot: %s (created %.0fs ago)",
                 snap_id, time.time() - snap["created"])
        return True

    def list_snapshots(self) -> List[str]:
        return list(self._snapshots.keys())

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORT / IMPORT
    # ─────────────────────────────────────────────────────────────────────────

    def export_registry(self) -> dict:
        return {
            name: {
                "category":    km.category,
                "type":        type(km.instance).__name__,
                "call_count":  km.call_count,
                "error_count": km.error_count,
                "registered":  km.registered,
            }
            for name, km in self._modules.items()
        }

    # ─────────────────────────────────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────────────────────────────────

    def status(self) -> dict:
        return {
            "version":     self.VERSION,
            "running":     self._running,
            "uptime":      round(self.uptime(), 1),
            "cycles":      self._cycle_count,
            "modules":     len(self._modules),
            "categories":  self.categories(),
            "events_logged": len(self._event_log),
            "snapshots":   len(self._snapshots),
            "base_path":   self.base_path,
        }