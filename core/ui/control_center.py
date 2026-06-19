# C:\Umbra\core\gui\control_center.py   AND   C:\Umbra\core\ui\umbra_control_center.py
# Copy this file to BOTH locations.
# Umbra GUI Control Center v2.0 — Full working tkinter GUI
# FIXED: _log was incomplete, all methods now fully implemented

import os
import sys
import json
import time
import queue
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

_UMBRA_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─────────────────────────────────────────────────────────────────────────────
# Colour scheme (dark theme)
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "bg":       "#0d0d1a",
    "panel":    "#13132a",
    "border":   "#2a2a5a",
    "accent":   "#6a40d4",
    "accent2":  "#4060c0",
    "green":    "#30c060",
    "red":      "#c03040",
    "yellow":   "#c0a020",
    "text":     "#d0d0e8",
    "dim":      "#707090",
    "input_bg": "#1a1a30",
    "btn":      "#2a2a50",
    "btn_h":    "#3a3a70",
    "log_bg":   "#0a0a18",
    "log_text": "#a0c0a0",
}

FONT_MONO  = ("Consolas", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_SMALL = ("Consolas", 9)


class UmbraControlCenter(tk.Tk):
    """
    Umbra GUI Control Center.

    Wired to Umbra's runtime via:
      - _output_queue: thread-safe queue; Umbra posts log messages here
      - post_message(text): called by Umbra runtime to display output
      - submit_command(text): sends command to Umbra's _process_command()
    """

    def __init__(self, runtime=None, process_fn=None):
        super().__init__()
        self.runtime     = runtime
        self.process_fn  = process_fn       # _process_command from Umbra.py
        self._out_queue  = queue.Queue()    # Umbra -> GUI messages
        self._cmd_queue  = queue.Queue()    # GUI -> Umbra commands
        self._history    = []               # command history
        self._hist_idx   = -1
        self._workspace  = os.path.join(_UMBRA_ROOT, "workspaces")
        self._running    = True

        self._setup_window()
        self._build_ui()
        self._start_queue_drain()
        self.log("[UMBRA] Control Center ready.", colour=C["green"])

    # ─────────────────────────────────────────────────────────────────────────
    # WINDOW SETUP
    # ─────────────────────────────────────────────────────────────────────────

    def _setup_window(self):
        self.title("UMBRA — Autonomous AI Runtime OS v2.3.0")
        self.configure(bg=C["bg"])
        self.geometry("1280x800")
        self.minsize(900, 600)
        try:
            self.iconbitmap(os.path.join(_UMBRA_ROOT, "core", "assets", "umbra.ico"))
        except Exception:
            pass
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─────────────────────────────────────────────────────────────────────────
    # UI BUILD
    # ─────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Title bar ────────────────────────────────────────────────────────
        title_frame = tk.Frame(self, bg=C["panel"], height=48)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="⬡  UMBRA", font=FONT_TITLE,
                 fg=C["accent"], bg=C["panel"]).pack(side=tk.LEFT, padx=16, pady=10)
        tk.Label(title_frame, text="Autonomous AI Runtime OS",
                 font=FONT_LABEL, fg=C["dim"], bg=C["panel"]).pack(side=tk.LEFT)
        self._status_lbl = tk.Label(title_frame, text="● READY",
                                    font=FONT_LABEL, fg=C["green"], bg=C["panel"])
        self._status_lbl.pack(side=tk.RIGHT, padx=16)

        # ── Main paned layout ─────────────────────────────────────────────────
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=C["bg"],
                               sashwidth=5, sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Left sidebar
        left = tk.Frame(paned, bg=C["panel"], width=200)
        paned.add(left, minsize=160)
        self._build_sidebar(left)

        # Main area (notebook tabs)
        right = tk.Frame(paned, bg=C["bg"])
        paned.add(right, minsize=600)
        self._build_main_area(right)

    # ── SIDEBAR ───────────────────────────────────────────────────────────────

    def _build_sidebar(self, parent):
        tk.Label(parent, text="QUICK ACTIONS", font=FONT_SMALL,
                 fg=C["dim"], bg=C["panel"]).pack(pady=(12, 4), padx=8, anchor="w")

        actions = [
            ("🔧 Fix All Bugs",         "fix all bugs"),
            ("📊 Status",               "status"),
            ("🎮 Build Game",           "build a full game called MyGame"),
            ("🖼 Make Image",           "make an image of a fantasy landscape"),
            ("🎬 Make GIF",             "make a gif of a dragon flying"),
            ("📁 List Files",           "list files"),
            ("🧹 Clean Old Files",      "clean up old files"),
            ("💾 List Projects",        "projects"),
            ("🔍 Scan Modules",         "scan modules"),
            ("📋 Help / Commands",      "help"),
        ]
        for label, cmd in actions:
            b = tk.Button(parent, text=label, font=FONT_SMALL,
                          fg=C["text"], bg=C["btn"], activebackground=C["btn_h"],
                          activeforeground=C["text"], relief=tk.FLAT,
                          cursor="hand2", anchor="w", padx=10,
                          command=lambda c=cmd: self._quick_action(c))
            b.pack(fill=tk.X, padx=6, pady=2)

        # Separator
        tk.Frame(parent, bg=C["border"], height=1).pack(fill=tk.X, padx=8, pady=10)
        tk.Label(parent, text="SYSTEM", font=FONT_SMALL,
                 fg=C["dim"], bg=C["panel"]).pack(padx=8, anchor="w")

        sys_btns = [
            ("▶ Play Last Game",  "run last"),
            ("🔄 Restart Umbra",  "__restart__"),
            ("✖ Close GUI",       "__close__"),
        ]
        for label, cmd in sys_btns:
            b = tk.Button(parent, text=label, font=FONT_SMALL,
                          fg=C["text"], bg=C["btn"], activebackground=C["btn_h"],
                          activeforeground=C["text"], relief=tk.FLAT,
                          cursor="hand2", anchor="w", padx=10,
                          command=lambda c=cmd: self._sys_action(c))
            b.pack(fill=tk.X, padx=6, pady=2)

        # Bottom status block
        tk.Frame(parent, bg=C["border"], height=1).pack(fill=tk.X, padx=8, pady=10)
        self._sidebar_status = tk.Label(parent, text="Model: qwen2.5-coder:32b\nOllama: checking...",
                                        font=FONT_SMALL, fg=C["dim"], bg=C["panel"],
                                        justify=tk.LEFT, wraplength=180)
        self._sidebar_status.pack(padx=8, anchor="w")

    # ── MAIN AREA TABS ────────────────────────────────────────────────────────

    def _build_main_area(self, parent):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=C["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=C["btn"], foreground=C["dim"],
                        font=FONT_LABEL, padding=[12, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", C["accent"])],
                  foreground=[("selected", "#ffffff")])

        self._nb = ttk.Notebook(parent)
        self._nb.pack(fill=tk.BOTH, expand=True)

        self._tab_chat    = tk.Frame(self._nb, bg=C["bg"])
        self._tab_tasks   = tk.Frame(self._nb, bg=C["bg"])
        self._tab_files   = tk.Frame(self._nb, bg=C["bg"])
        self._tab_agents  = tk.Frame(self._nb, bg=C["bg"])
        self._tab_memory  = tk.Frame(self._nb, bg=C["bg"])

        self._nb.add(self._tab_chat,   text="  💬 Chat / Console  ")
        self._nb.add(self._tab_tasks,  text="  📋 Task Queue  ")
        self._nb.add(self._tab_files,  text="  📁 Files  ")
        self._nb.add(self._tab_agents, text="  🤖 Agents  ")
        self._nb.add(self._tab_memory, text="  🧠 Memory  ")

        self._build_chat_tab(self._tab_chat)
        self._build_tasks_tab(self._tab_tasks)
        self._build_files_tab(self._tab_files)
        self._build_agents_tab(self._tab_agents)
        self._build_memory_tab(self._tab_memory)

    # ── CHAT TAB ─────────────────────────────────────────────────────────────

    def _build_chat_tab(self, parent):
        # Output log
        log_frame = tk.Frame(parent, bg=C["bg"])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self._log = scrolledtext.ScrolledText(
            log_frame, bg=C["log_bg"], fg=C["log_text"],
            font=FONT_MONO, wrap=tk.WORD, state=tk.DISABLED,
            relief=tk.FLAT, borderwidth=0, insertbackground=C["text"],
        )
        self._log.pack(fill=tk.BOTH, expand=True)

        # Tag colours for log
        self._log.tag_config("green",  foreground=C["green"])
        self._log.tag_config("red",    foreground=C["red"])
        self._log.tag_config("yellow", foreground=C["yellow"])
        self._log.tag_config("accent", foreground=C["accent"])
        self._log.tag_config("dim",    foreground=C["dim"])
        self._log.tag_config("white",  foreground=C["text"])

        # Input area
        input_frame = tk.Frame(parent, bg=C["panel"], pady=8)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=6, pady=(0, 6))

        tk.Label(input_frame, text="umbra >", font=FONT_MONO,
                 fg=C["accent"], bg=C["panel"]).pack(side=tk.LEFT, padx=(8, 4))

        self._input = tk.Entry(input_frame, bg=C["input_bg"], fg=C["text"],
                               font=FONT_MONO, relief=tk.FLAT, insertbackground=C["text"],
                               highlightthickness=1, highlightbackground=C["border"],
                               highlightcolor=C["accent"])
        self._input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        self._input.bind("<Return>",    self._on_enter)
        self._input.bind("<Up>",        self._hist_up)
        self._input.bind("<Down>",      self._hist_down)
        self._input.focus_set()

        send_btn = tk.Button(input_frame, text="Send ▶", font=FONT_LABEL,
                             fg="#ffffff", bg=C["accent"],
                             activebackground=C["accent2"], relief=tk.FLAT,
                             padx=12, cursor="hand2", command=self._on_enter)
        send_btn.pack(side=tk.RIGHT, padx=(4, 8))

    # ── TASKS TAB ────────────────────────────────────────────────────────────

    def _build_tasks_tab(self, parent):
        tk.Label(parent, text="Task Queue & History", font=FONT_LABEL,
                 fg=C["dim"], bg=C["bg"]).pack(pady=8, anchor="w", padx=10)

        cols = ("Task", "Type", "Status", "Time")
        self._task_tree = ttk.Treeview(parent, columns=cols, show="headings", height=20)
        for c in cols:
            self._task_tree.heading(c, text=c)
            self._task_tree.column(c, width=200 if c == "Task" else 100)

        sb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self._task_tree.yview)
        self._task_tree.configure(yscrollcommand=sb.set)
        self._task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=4)
        sb.pack(side=tk.LEFT, fill=tk.Y, pady=4)

        btn_frame = tk.Frame(parent, bg=C["bg"])
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        tk.Button(btn_frame, text="Refresh", font=FONT_SMALL,
                  fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=10,
                  command=self._refresh_tasks).pack(pady=4, fill=tk.X)
        tk.Button(btn_frame, text="Clear Done", font=FONT_SMALL,
                  fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=10,
                  command=self._clear_tasks).pack(pady=4, fill=tk.X)

    # ── FILES TAB ────────────────────────────────────────────────────────────

    def _build_files_tab(self, parent):
        tk.Label(parent, text="Workspace Files", font=FONT_LABEL,
                 fg=C["dim"], bg=C["bg"]).pack(pady=8, anchor="w", padx=10)

        # Toolbar
        bar = tk.Frame(parent, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0, 4))
        tk.Button(bar, text="🔄 Refresh", font=FONT_SMALL, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._refresh_files).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="📂 Open Folder", font=FONT_SMALL, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._open_workspace).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="▶ Run Selected", font=FONT_SMALL, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._run_selected).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="🗑 Delete Selected", font=FONT_SMALL, fg=C["red"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._delete_selected).pack(side=tk.LEFT, padx=2)

        # File tree
        cols = ("Name", "Size", "Modified", "Type")
        self._file_tree = ttk.Treeview(parent, columns=cols, show="headings", height=22)
        for c in cols:
            self._file_tree.heading(c, text=c)
        self._file_tree.column("Name", width=280)
        self._file_tree.column("Size", width=80)
        self._file_tree.column("Modified", width=140)
        self._file_tree.column("Type", width=80)

        sb2 = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self._file_tree.yview)
        self._file_tree.configure(yscrollcommand=sb2.set)
        self._file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=4)
        sb2.pack(side=tk.LEFT, fill=tk.Y, pady=4)
        self._file_tree.bind("<Double-1>", self._on_file_double_click)
        self._refresh_files()

    # ── AGENTS TAB ───────────────────────────────────────────────────────────

    def _build_agents_tab(self, parent):
        tk.Label(parent, text="Agent Status", font=FONT_LABEL,
                 fg=C["dim"], bg=C["bg"]).pack(pady=8, anchor="w", padx=10)

        agents = [
            ("World Agent",     "Generates game world, biomes, maps"),
            ("Character Agent", "Player, enemy, NPC classes and stats"),
            ("Item Agent",      "Weapons, armor, spells, loot tables"),
            ("Mechanic Agent",  "Combat, crafting, quests systems"),
            ("UI Agent",        "HUD, menus, inventory, dialogue panels"),
            ("Quest Agent",     "Quest data, spawn logic, progression"),
            ("Economy Agent",   "Shops, crafting recipes, building costs"),
            ("Image Agent",     "ComfyUI image generation pipeline"),
            ("Sprite Agent",    "PIL pixel-art sprite generator"),
            ("GIF Agent",       "PIL animated GIF generator"),
            ("TTS Agent",       "Text-to-speech via pyttsx3"),
            ("Voice Agent",     "Speech recognition input"),
            ("Code Agent",      "Ollama code generation pipeline"),
            ("Repair Agent",    "Syntax checking and auto-repair"),
        ]
        frame = tk.Frame(parent, bg=C["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        cols = ("Agent", "Description", "Status")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=20)
        tree.heading("Agent",       text="Agent")
        tree.heading("Description", text="Description")
        tree.heading("Status",      text="Status")
        tree.column("Agent",       width=160)
        tree.column("Description", width=380)
        tree.column("Status",      width=100)

        for name, desc in agents:
            tree.insert("", tk.END, values=(name, desc, "standby"))

        sb3 = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb3.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb3.pack(side=tk.LEFT, fill=tk.Y)
        self._agent_tree = tree

    # ── MEMORY TAB ───────────────────────────────────────────────────────────

    def _build_memory_tab(self, parent):
        tk.Label(parent, text="Runtime Memory", font=FONT_LABEL,
                 fg=C["dim"], bg=C["bg"]).pack(pady=8, anchor="w", padx=10)

        bar = tk.Frame(parent, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0, 4))
        tk.Button(bar, text="🔄 Refresh", font=FONT_SMALL, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._refresh_memory).pack(side=tk.LEFT, padx=2)
        tk.Label(bar, text="Search:", fg=C["dim"], bg=C["bg"],
                 font=FONT_SMALL).pack(side=tk.LEFT, padx=(10, 4))
        self._mem_search = tk.Entry(bar, bg=C["input_bg"], fg=C["text"],
                                    font=FONT_SMALL, width=30, relief=tk.FLAT)
        self._mem_search.pack(side=tk.LEFT)
        self._mem_search.bind("<Return>", lambda e: self._refresh_memory())

        cols = ("Key", "Value", "Tags")
        self._mem_tree = ttk.Treeview(parent, columns=cols, show="headings", height=22)
        self._mem_tree.heading("Key",   text="Key")
        self._mem_tree.heading("Value", text="Value")
        self._mem_tree.heading("Tags",  text="Tags")
        self._mem_tree.column("Key",   width=200)
        self._mem_tree.column("Value", width=360)
        self._mem_tree.column("Tags",  width=160)

        sb4 = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self._mem_tree.yview)
        self._mem_tree.configure(yscrollcommand=sb4.set)
        self._mem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=4)
        sb4.pack(side=tk.LEFT, fill=tk.Y, pady=4)

    # ─────────────────────────────────────────────────────────────────────────
    # LOGGING — thread-safe
    # ─────────────────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        """Internal alias; kept for backward compatibility."""
        self.log(msg)

    def log(self, msg: str, colour: str = None):
        """Post a message to the output log (thread-safe)."""
        self._out_queue.put(("log", str(msg), colour))

    def post_message(self, text: str):
        """Called by Umbra runtime to push output into the GUI."""
        self.log(text)

    def _drain_queue(self):
        """Drain the output queue and write to the log widget."""
        try:
            while True:
                item = self._out_queue.get_nowait()
                if item[0] == "log":
                    _, msg, colour = item
                    self._write_log(msg, colour)
        except queue.Empty:
            pass
        if self._running:
            self.after(80, self._drain_queue)

    def _write_log(self, msg: str, colour: str = None):
        self._log.configure(state=tk.NORMAL)
        ts  = time.strftime("%H:%M:%S")
        tag = "white"
        # Auto-colour based on message prefix
        low = msg.lower()
        if colour:
            # Map hex colour to tag name
            rev = {C["green"]: "green", C["red"]: "red",
                   C["yellow"]: "yellow", C["accent"]: "accent"}
            tag = rev.get(colour, "white")
        elif any(x in low for x in ("[error]", "[fail]", "[broken]", "failed")):
            tag = "red"
        elif any(x in low for x in ("[ok]", "[done]", "[success]", "complete", "saved", "ready")):
            tag = "green"
        elif any(x in low for x in ("[warn]", "[warning]", "missing", "not available")):
            tag = "yellow"
        elif any(x in low for x in ("[umbra]", "[build]", "[plan]", "[agent]")):
            tag = "accent"
        elif msg.startswith("  ") or msg.startswith("["):
            tag = "dim"

        self._log.insert(tk.END, f"[{ts}] {msg}\n", tag)
        self._log.see(tk.END)
        self._log.configure(state=tk.DISABLED)

    def _start_queue_drain(self):
        self.after(80, self._drain_queue)

    # ─────────────────────────────────────────────────────────────────────────
    # COMMAND INPUT
    # ─────────────────────────────────────────────────────────────────────────

    def _on_enter(self, event=None):
        text = self._input.get().strip()
        if not text:
            return
        self._input.delete(0, tk.END)
        # History
        if not self._history or self._history[-1] != text:
            self._history.append(text)
        self._hist_idx = len(self._history)
        # Echo to log
        self.log(f"you > {text}", colour=C["accent"])
        # Send command
        self._send_command(text)

    def _send_command(self, text: str):
        """Send a command to Umbra in a background thread."""
        def _run():
            try:
                if self.process_fn and callable(self.process_fn):
                    self.process_fn(self.runtime, text)
                elif self.runtime:
                    # Try common patterns
                    for attr in ("run_prompt", "process", "handle"):
                        fn = getattr(self.runtime, attr, None)
                        if fn:
                            fn(text)
                            return
                    self.log("[GUI] No process function connected to runtime.", colour=C["yellow"])
                else:
                    self.log("[GUI] Runtime not connected.", colour=C["yellow"])
            except Exception as e:
                self.log(f"[ERROR] Command failed: {e}", colour=C["red"])

        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def _quick_action(self, cmd: str):
        self._input.delete(0, tk.END)
        self._input.insert(0, cmd)
        self._on_enter()

    def _sys_action(self, cmd: str):
        if cmd == "__close__":
            self._on_close()
        elif cmd == "__restart__":
            self.log("[GUI] Restarting Umbra...", colour=C["yellow"])
            self.after(500, lambda: subprocess.Popen(
                [sys.executable, os.path.join(_UMBRA_ROOT, "Umbra.py")],
                cwd=_UMBRA_ROOT))
        else:
            self._quick_action(cmd)

    def _hist_up(self, event=None):
        if not self._history:
            return
        self._hist_idx = max(0, self._hist_idx - 1)
        self._input.delete(0, tk.END)
        self._input.insert(0, self._history[self._hist_idx])

    def _hist_down(self, event=None):
        if not self._history:
            return
        self._hist_idx = min(len(self._history), self._hist_idx + 1)
        self._input.delete(0, tk.END)
        if self._hist_idx < len(self._history):
            self._input.insert(0, self._history[self._hist_idx])

    # ─────────────────────────────────────────────────────────────────────────
    # TASKS TAB LOGIC
    # ─────────────────────────────────────────────────────────────────────────

    def _refresh_tasks(self):
        for item in self._task_tree.get_children():
            self._task_tree.delete(item)
        if not self.runtime:
            return
        # Pull from task engine if available
        spine = getattr(self.runtime, "spine", None)
        if spine:
            for r in spine.get_history()[-50:]:
                ts = time.strftime("%H:%M:%S", time.localtime(r.get("timestamp", 0)))
                self._task_tree.insert("", tk.END, values=(
                    r.get("prompt", "")[:60],
                    r.get("task_type", "?"),
                    r.get("status", "?"),
                    ts,
                ))

    def _clear_tasks(self):
        for item in self._task_tree.get_children():
            self._task_tree.delete(item)

    # ─────────────────────────────────────────────────────────────────────────
    # FILES TAB LOGIC
    # ─────────────────────────────────────────────────────────────────────────

    def _refresh_files(self):
        for item in self._file_tree.get_children():
            self._file_tree.delete(item)
        ws = self._workspace
        if not os.path.isdir(ws):
            return
        for root, dirs, files in os.walk(ws):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "venv")]
            level = root.replace(ws, "").count(os.sep)
            if level > 2:
                continue
            rel = os.path.relpath(root, ws)
            if rel != ".":
                self._file_tree.insert("", tk.END, values=(
                    "📁 " + rel + "/", "", "", "folder"))
            for fname in sorted(files)[:40]:
                fp = os.path.join(root, fname)
                try:
                    sz  = os.path.getsize(fp)
                    mod = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(fp)))
                    ext = os.path.splitext(fname)[1]
                    sz_str = f"{sz//1024}KB" if sz > 1024 else f"{sz}B"
                    self._file_tree.insert("", tk.END,
                                           values=(fname, sz_str, mod, ext),
                                           tags=(fp,))
                except Exception:
                    pass

    def _open_workspace(self):
        ws = self._workspace
        os.makedirs(ws, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(ws)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", ws])
        else:
            subprocess.Popen(["xdg-open", ws])

    def _run_selected(self):
        sel = self._file_tree.selection()
        if not sel:
            return
        tags = self._file_tree.item(sel[0], "tags")
        if tags:
            fp = tags[0]
            if fp.endswith(".py") and os.path.isfile(fp):
                subprocess.Popen([sys.executable, fp], cwd=os.path.dirname(fp))
                self.log(f"[GUI] Launched: {fp}", colour=C["green"])

    def _delete_selected(self):
        sel = self._file_tree.selection()
        if not sel:
            return
        tags = self._file_tree.item(sel[0], "tags")
        if not tags:
            return
        fp = tags[0]
        if not os.path.isfile(fp):
            return
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(fp)}?"):
            try:
                os.remove(fp)
                self.log(f"[GUI] Deleted: {fp}", colour=C["yellow"])
                self._refresh_files()
            except Exception as e:
                self.log(f"[ERROR] Delete failed: {e}", colour=C["red"])

    def _on_file_double_click(self, event=None):
        self._run_selected()

    # ─────────────────────────────────────────────────────────────────────────
    # MEMORY TAB LOGIC
    # ─────────────────────────────────────────────────────────────────────────

    def _refresh_memory(self):
        for item in self._mem_tree.get_children():
            self._mem_tree.delete(item)
        if not self.runtime:
            return
        mem = None
        if isinstance(self.runtime, dict):
            mem = self.runtime.get("memory")
        else:
            mem = getattr(self.runtime, "memory", None)
        if not mem:
            return
        query = self._mem_search.get().strip().lower()
        try:
            entries = mem.list_all() if hasattr(mem, "list_all") else []
        except Exception:
            entries = []
        for entry in entries:
            key   = str(entry.get("key",   ""))
            value = str(entry.get("value", ""))[:120]
            tags  = str(entry.get("tags",  ""))
            if query and query not in key.lower() and query not in value.lower():
                continue
            self._mem_tree.insert("", tk.END, values=(key, value, tags))

    # ─────────────────────────────────────────────────────────────────────────
    # CLOSE
    # ─────────────────────────────────────────────────────────────────────────

    def _on_close(self):
        self._running = False
        try:
            self.destroy()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Standalone launch (for testing)
# ─────────────────────────────────────────────────────────────────────────────
def launch_control_center(runtime=None, process_fn=None):
    """Launch the GUI in the main thread. Called from Umbra._launch_gui()."""
    app = UmbraControlCenter(runtime=runtime, process_fn=process_fn)
    app.mainloop()
    return app


def launch_in_thread(runtime=None, process_fn=None):
    """Launch GUI in a daemon thread (non-blocking)."""
    ref = [None]

    def _run():
        ref[0] = UmbraControlCenter(runtime=runtime, process_fn=process_fn)
        ref[0].mainloop()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    # Wait briefly for window to appear
    for _ in range(20):
        time.sleep(0.1)
        if ref[0] is not None:
            break
    return ref[0]


if __name__ == "__main__":
    # Test mode — runs with no runtime
    app = UmbraControlCenter()
    app.log("Umbra Control Center — test mode", colour=C["green"])
    app.log("No runtime connected. Commands will echo only.", colour=C["yellow"])
    app.mainloop()