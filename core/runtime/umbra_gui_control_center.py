import threading
import queue
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext


class UmbraGUIControlCenter:
    """
    Live control surface for Umbra runtime:
    - view logs
    - trigger cycles
    - approve patches
    - monitor agent activity
    """

    def __init__(self, runtime_kernel):
        self.kernel = runtime_kernel
        self.event_queue = queue.Queue()
        self.root = tk.Tk()
        self.root.title("Umbra Control Center")

        self._build_ui()
        self._start_event_loop()

    # ---------------- UI ----------------

    def _build_ui(self):
        self.log_box = scrolledtext.ScrolledText(self.root, width=120, height=30)
        self.log_box.pack()

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Run Cycle", command=self.run_cycle).pack(side="left")
        ttk.Button(btn_frame, text="Snapshot", command=self.snapshot).pack(side="left")
        ttk.Button(btn_frame, text="Shutdown", command=self.shutdown).pack(side="left")

    # ---------------- Actions ----------------

    def run_cycle(self):
        result = self.kernel.run_cycle()
        self._log(f"[CYCLE] {json.dumps(result, indent=2)}")

    def snapshot(self):
        snap = self.kernel.snapshot()
        self._log(f"[SNAPSHOT] {snap}")

    def shutdown(self):
        self._log("[SYSTEM] Shutdown requested")
        self.kernel.shutdown()
        self.root.destroy()

    # ---------------- Logging ----------------

    def _log(self, msg: str):
        self.event_queue.put(msg)

    def _start_event_loop(self):
        def loop():
            while True:
                try:
                    msg = self.event_queue.get_nowait()
                    self.log_box.insert(tk.END, msg + "\n")
                    self.log_box.see(tk.END)
                except queue.Empty:
                    break
            self.root.after(200, loop)

        loop()

    def start(self):
        self.root.mainloop()