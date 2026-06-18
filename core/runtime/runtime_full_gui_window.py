"""
RuntimeFullGuiWindow
Tkinter GUI window that opens alongside the CLI.
Chat box, status panel, TTS toggle, input field, progress bar.
Runs in its own thread so it doesn't block the CLI.
"""
import threading
import queue
import os
import sys


class RuntimeFullGuiWindow:
    def __init__(self, **kwargs):
        self.ready = True
        self._queue = queue.Queue()
        self._root = None
        self._chat_text = None
        self._input_var = None
        self._status_var = None
        self._tts_var = None
        self._progress_var = None
        self._submit_callback = None
        self._running = False
        try:
            import tkinter as tk
            self._tk = tk
        except ImportError:
            self.ready = False
            self._tk = None

    def is_available(self):
        return self.ready

    def set_submit_callback(self, fn):
        """Set function called when user submits input from GUI."""
        self._submit_callback = fn

    def add_message(self, role, text):
        """Add a message to the chat display (thread-safe)."""
        self._queue.put(("message", role, text))

    def set_status(self, text):
        """Update the status bar (thread-safe)."""
        self._queue.put(("status", text))

    def set_progress(self, pct):
        """Update progress bar 0-100 (thread-safe)."""
        self._queue.put(("progress", pct))

    def _process_queue(self):
        """Called by tkinter mainloop to process queued updates."""
        try:
            while True:
                item = self._queue.get_nowait()
                if item[0] == "message":
                    _, role, text = item
                    if self._chat_text:
                        self._chat_text.config(state="normal")
                        tag = "user" if role == "user" else "umbra"
                        prefix = "You: " if role == "user" else "Umbra: "
                        self._chat_text.insert("end", prefix + text + "\n", tag)
                        self._chat_text.see("end")
                        self._chat_text.config(state="disabled")
                elif item[0] == "status":
                    if self._status_var:
                        self._status_var.set(item[1])
                elif item[0] == "progress":
                    if self._progress_var:
                        self._progress_var.set(item[1])
        except queue.Empty:
            pass
        if self._running and self._root:
            self._root.after(100, self._process_queue)

    def _on_submit(self):
        if not self._input_var:
            return
        text = self._input_var.get().strip()
        if not text:
            return
        self._input_var.set("")
        self.add_message("user", text)
        if self._submit_callback:
            threading.Thread(target=self._submit_callback, args=(text,), daemon=True).start()

    def run(self, title="Umbra AI"):
        """Start the GUI window. Blocks until window is closed."""
        if not self.ready or not self._tk:
            return {"status": "error", "error": "tkinter not available"}

        tk = self._tk
        self._running = True

        root = tk.Tk()
        self._root = root
        root.title(title)
        root.geometry("800x600")
        root.configure(bg="#1a1a2e")

        # ── Title bar ──
        title_frame = tk.Frame(root, bg="#16213e", pady=8)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="UMBRA AI Runtime OS", font=("Consolas", 14, "bold"),
                 fg="#00d4ff", bg="#16213e").pack()

        # ── Status bar ──
        status_frame = tk.Frame(root, bg="#0f3460", pady=4)
        status_frame.pack(fill="x")
        self._status_var = tk.StringVar(value="Ready")
        tk.Label(status_frame, textvariable=self._status_var, font=("Consolas", 9),
                 fg="#a0a0c0", bg="#0f3460").pack(side="left", padx=10)

        # ── TTS toggle ──
        self._tts_var = tk.BooleanVar(value=False)
        tk.Checkbutton(status_frame, text="TTS", variable=self._tts_var,
                       font=("Consolas", 9), fg="#a0a0c0", bg="#0f3460",
                       selectcolor="#0f3460", activebackground="#0f3460").pack(side="right", padx=10)

        # ── Progress bar ──
        progress_frame = tk.Frame(root, bg="#1a1a2e", pady=2)
        progress_frame.pack(fill="x", padx=10)
        self._progress_var = tk.DoubleVar(value=0)
        try:
            from tkinter import ttk
            pb = ttk.Progressbar(progress_frame, variable=self._progress_var, maximum=100, length=780)
            pb.pack(fill="x")
        except Exception:
            pass

        # ── Chat display ──
        chat_frame = tk.Frame(root, bg="#1a1a2e")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side="right", fill="y")

        self._chat_text = tk.Text(
            chat_frame, bg="#0d1117", fg="#c9d1d9", font=("Consolas", 10),
            state="disabled", wrap="word", yscrollcommand=scrollbar.set,
            relief="flat", bd=0, insertbackground="#00d4ff"
        )
        self._chat_text.pack(fill="both", expand=True)
        self._chat_text.tag_config("user", foreground="#58a6ff")
        self._chat_text.tag_config("umbra", foreground="#3fb950")
        scrollbar.config(command=self._chat_text.yview)

        # ── Input area ──
        input_frame = tk.Frame(root, bg="#1a1a2e", pady=8)
        input_frame.pack(fill="x", padx=10)

        self._input_var = tk.StringVar()
        entry = tk.Entry(
            input_frame, textvariable=self._input_var,
            font=("Consolas", 11), bg="#161b22", fg="#c9d1d9",
            insertbackground="#00d4ff", relief="flat", bd=5
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6)
        entry.bind("<Return>", lambda e: self._on_submit())
        entry.focus_set()

        send_btn = tk.Button(
            input_frame, text="Send", command=self._on_submit,
            font=("Consolas", 10, "bold"), bg="#238636", fg="white",
            relief="flat", padx=16, pady=6, cursor="hand2"
        )
        send_btn.pack(side="right", padx=(8, 0))

        # Welcome message
        self.add_message("umbra", "Umbra GUI ready. Type naturally or use voice commands.")

        # Start queue processor
        root.after(100, self._process_queue)

        def on_close():
            self._running = False
            root.destroy()
            self._root = None

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()
        return {"status": "closed"}