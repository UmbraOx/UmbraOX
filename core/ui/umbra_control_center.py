import tkinter as tk
from tkinter import ttk, filedialog
import os
import time


class UmbraControlCenter:
    """
    Desktop GUI Control Center (NOT web)

    Features:
    - Task queue management
    - Asset preview (images/videos/audio placeholders)
    - TTS/STT toggles
    - Live execution monitor
    - Progress + ETA display
    """

    def __init__(self, spine, asset_dir="C:\\Umbra\\assets"):

        self.spine = spine
        self.asset_dir = asset_dir

        self.root = tk.Tk()
        self.root.title("Umbra Control Center")
        self.root.geometry("1200x800")
        self.root.configure(bg="#111111")

        self.dark_mode = True

        self._build_ui()

    # -------------------------
    # UI LAYOUT
    # -------------------------

    def _build_ui(self):

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        self.queue_tab = ttk.Frame(self.tabs)
        self.assets_tab = ttk.Frame(self.tabs)
        self.monitor_tab = ttk.Frame(self.tabs)
        self.voice_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.queue_tab, text="Task Queue")
        self.tabs.add(self.assets_tab, text="Assets Viewer")
        self.tabs.add(self.monitor_tab, text="Execution Monitor")
        self.tabs.add(self.voice_tab, text="Voice Controls")

        self._build_queue_tab()
        self._build_assets_tab()
        self._build_monitor_tab()
        self._build_voice_tab()

    # -------------------------
    # TASK QUEUE TAB
    # -------------------------

    def _build_queue_tab(self):

        self.queue_list = tk.Listbox(self.queue_tab, height=25, bg="#1a1a1a", fg="white")
        self.queue_list.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.queue_tab)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Refresh Queue", command=self.refresh_queue).pack(side="left")
        tk.Button(btn_frame, text="Move Up", command=self.move_up).pack(side="left")
        tk.Button(btn_frame, text="Move Down", command=self.move_down).pack(side="left")

    def refresh_queue(self):

        self.queue_list.delete(0, tk.END)

        queue = getattr(self.spine.boss_agent.queue, "items", [])

        for i, task in enumerate(queue):
            self.queue_list.insert(tk.END, f"{i}: {task}")

    def move_up(self):
        pass

    def move_down(self):
        pass

    # -------------------------
    # ASSET VIEWER TAB
    # -------------------------

    def _build_assets_tab(self):

        self.asset_list = tk.Listbox(self.assets_tab, bg="#1a1a1a", fg="white")
        self.asset_list.pack(side="left", fill="y")

        self.preview = tk.Label(self.assets_tab, text="Preview Area", bg="#222", fg="white")
        self.preview.pack(fill="both", expand=True)

        tk.Button(self.assets_tab, text="Load Assets", command=self.load_assets).pack()

    def load_assets(self):

        self.asset_list.delete(0, tk.END)

        if not os.path.exists(self.asset_dir):
            os.makedirs(self.asset_dir)

        for file in os.listdir(self.asset_dir):
            self.asset_list.insert(tk.END, file)

    # -------------------------
    # MONITOR TAB
    # -------------------------

    def _build_monitor_tab(self):

        self.progress = ttk.Progressbar(self.monitor_tab, length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.eta_label = tk.Label(self.monitor_tab, text="ETA: --", bg="#111", fg="white")
        self.eta_label.pack()

        self.status_label = tk.Label(self.monitor_tab, text="Status: Idle", bg="#111", fg="white")
        self.status_label.pack()

        self._update_monitor()

    def _update_monitor(self):

        cycle = getattr(self.spine, "cycle_index", 0)

        progress_value = (cycle % 100)
        self.progress["value"] = progress_value

        eta = max(0, 100 - progress_value)

        self.eta_label.config(text=f"ETA cycles: {eta}")
        self.status_label.config(text=f"Cycle: {cycle}")

        self.root.after(1000, self._update_monitor)

    # -------------------------
    # VOICE TAB (TTS / STT)
    # -------------------------

    def _build_voice_tab(self):

        self.tts_enabled = tk.BooleanVar()
        self.stt_enabled = tk.BooleanVar()

        tk.Checkbutton(
            self.voice_tab,
            text="Enable TTS",
            variable=self.tts_enabled
        ).pack(anchor="w")

        tk.Checkbutton(
            self.voice_tab,
            text="Enable Voice Input (STT)",
            variable=self.stt_enabled
        ).pack(anchor="w")

        tk.Button(self.voice_tab, text="Test Voice", command=self.test_voice).pack()

    def test_voice(self):
        print("Voice test triggered (wire to TTS engine)")

    # -------------------------
    # RUN
    # -------------------------

    def run(self):
        self.root.mainloop()