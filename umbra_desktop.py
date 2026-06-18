"""
UMBRA Desktop App v1.0
A proper desktop window for Umbra — no browser needed.
Run: python umbra_desktop.py
"""

import sys
import os
import threading
import json
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime

_UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)

# Colors
BG = "#0d0d0d"
BG2 = "#111122"
BG3 = "#0a0a1a"
ACCENT = "#7c83fd"
GREEN = "#4caf50"
RED = "#f44336"
ORANGE = "#ff9800"
TEXT = "#e0e0e0"
MUTED = "#666666"
BORDER = "#222244"


class UmbraDesktop:

    def __init__(self, root):
        self.root = root
        self.root.title("UMBRA v2.0 — Autonomous AI Runtime OS")
        self.root.geometry("1280x800")
        self.root.configure(bg=BG)
        self.root.minsize(900, 600)

        self.runtime = None
        self.runtime_ready = False
        self._run_counter = 0

        self._build_ui()
        self._start_runtime()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a2e", height=44)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="◆ UMBRA v2.0 — Autonomous AI Runtime OS",
                 bg="#1a1a2e", fg=ACCENT, font=("Segoe UI", 12, "bold")).pack(side="left", padx=16, pady=8)
        self.status_label = tk.Label(header, text="● Starting...", bg="#1a1a2e", fg=ORANGE,
                                      font=("Segoe UI", 9))
        self.status_label.pack(side="right", padx=16)
        self.model_label = tk.Label(header, text="", bg="#1a1a2e", fg=MUTED, font=("Segoe UI", 9))
        self.model_label.pack(side="right", padx=8)

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg=BG2, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="SYSTEM", bg=BG2, fg=ACCENT,
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=12, pady=(14, 4))

        self.stat_provider = self._sidebar_stat(sidebar, "Provider", "-")
        self.stat_model = self._sidebar_stat(sidebar, "Model", "-")
        self.stat_runs = self._sidebar_stat(sidebar, "Runs", "0")
        self.stat_memory = self._sidebar_stat(sidebar, "Memory", "0")
        self.stat_ram = self._sidebar_stat(sidebar, "RAM", "0%")

        self.gaming_frame = tk.Frame(sidebar, bg="#2a1a00", bd=1, relief="solid")
        tk.Label(self.gaming_frame, text="🎮 Gaming Mode Active\nUmbra at IDLE priority",
                 bg="#2a1a00", fg=ORANGE, font=("Segoe UI", 8), justify="center").pack(padx=6, pady=4)

        tk.Label(sidebar, text="ACTIONS", bg=BG2, fg=ACCENT,
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=12, pady=(14, 4))

        actions = [
            ("● Health Check", self.do_health),
            ("📊 View Metrics", lambda: self.switch_tab("metrics")),
            ("📁 Browse Files", lambda: self.switch_tab("files")),
            ("✓ Validate Last", self.do_validate),
            ("🔍 Review Last", self.do_review),
        ]
        for label, cmd in actions:
            btn = tk.Button(sidebar, text=label, bg=BG2, fg="#ccc",
                           font=("Segoe UI", 9), bd=0, padx=10, pady=5,
                           anchor="w", cursor="hand2", activebackground="#30305a",
                           activeforeground="white", command=cmd)
            btn.pack(fill="x", padx=8, pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#30305a"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG2))

        tk.Label(sidebar, text="v2.0.0 • 608 tests\nGaming priority: ON\nAuto-save: ON",
                 bg=BG2, fg=MUTED, font=("Segoe UI", 7), justify="left").pack(
                     anchor="w", padx=12, pady=12)

        # Content area
        content = tk.Frame(main, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        # Tab bar
        tab_bar = tk.Frame(content, bg=BG2, height=36)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        self.tabs = {}
        self.tab_buttons = {}
        self.current_tab = "chat"

        for name, label in [("chat","💬 Chat"), ("metrics","📊 Metrics"),
                              ("health","● Health"), ("files","📁 Files"),
                              ("memory","🧠 Memory"), ("settings","⚙ Settings")]:
            btn = tk.Label(tab_bar, text=label, bg=BG2, fg=MUTED,
                           font=("Segoe UI", 9), padx=14, pady=8, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, n=name: self.switch_tab(n))
            self.tab_buttons[name] = btn

        self.tab_frame = tk.Frame(content, bg=BG)
        self.tab_frame.pack(fill="both", expand=True)

        self._build_chat_tab()
        self._build_metrics_tab()
        self._build_health_tab()
        self._build_files_tab()
        self._build_memory_tab()
        self._build_settings_tab()

        self.switch_tab("chat")
        self._update_status_bar_loop()

    def _sidebar_stat(self, parent, label, default):
        frame = tk.Frame(parent, bg=BG2)
        frame.pack(fill="x", padx=10, pady=1)
        tk.Label(frame, text=label, bg=BG2, fg=MUTED, font=("Segoe UI", 8)).pack(side="left")
        var = tk.StringVar(value=default)
        tk.Label(frame, textvariable=var, bg=BG2, fg=ACCENT,
                 font=("Segoe UI", 8, "bold")).pack(side="right")
        return var

    def _build_chat_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["chat"] = frame

        self.chat_output = scrolledtext.ScrolledText(
            frame, bg=BG3, fg=TEXT, font=("Consolas", 9),
            wrap="word", bd=0, padx=10, pady=10,
            insertbackground=ACCENT, state="disabled"
        )
        self.chat_output.pack(fill="both", expand=True, padx=10, pady=(10, 6))

        self.chat_output.tag_configure("user", foreground="#a0a8ff")
        self.chat_output.tag_configure("umbra", foreground=TEXT)
        self.chat_output.tag_configure("system", foreground=MUTED)
        self.chat_output.tag_configure("success", foreground=GREEN)
        self.chat_output.tag_configure("error", foreground=RED)
        self.chat_output.tag_configure("file", foreground=MUTED)

        self._chat_msg("UMBRA v2.0 Desktop ready. Type any objective below and press Enter.", "system")
        self._chat_msg("Examples: 'write a pygame game' | 'build a REST API' | 'analyze CSV data'", "system")

        input_frame = tk.Frame(frame, bg=BG)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.chat_input = tk.Entry(input_frame, bg=BG2, fg=TEXT,
                                    font=("Segoe UI", 10), bd=0,
                                    insertbackground=ACCENT,
                                    highlightthickness=1,
                                    highlightcolor=ACCENT,
                                    highlightbackground=BORDER)
        self.chat_input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.chat_input.bind("<Return>", lambda e: self.send_prompt())
        self.chat_input.bind("<FocusIn>", lambda e: self.chat_input.configure(highlightcolor=ACCENT))

        self.run_btn = tk.Button(input_frame, text="Run", bg=ACCENT, fg="white",
                                  font=("Segoe UI", 9, "bold"), bd=0, padx=16, pady=8,
                                  cursor="hand2", command=self.send_prompt)
        self.run_btn.pack(side="left")

        tk.Button(input_frame, text="Clear", bg=BG2, fg="#ccc",
                  font=("Segoe UI", 9), bd=0, padx=12, pady=8,
                  cursor="hand2", command=self.clear_chat).pack(side="left", padx=(4, 0))

    def _build_metrics_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["metrics"] = frame

        cards_frame = tk.Frame(frame, bg=BG)
        cards_frame.pack(fill="x", padx=10, pady=10)

        self.metric_vars = {}
        metrics = [("Total Runs","total"), ("Successful","ok"), ("Success Rate","rate"),
                   ("Files Written","files"), ("Tasks Run","tasks"), ("Avg Duration","dur")]
        for i, (label, key) in enumerate(metrics):
            card = tk.Frame(cards_frame, bg=BG2, bd=1, relief="solid")
            card.grid(row=i//3, column=i%3, padx=4, pady=4, sticky="nsew")
            cards_frame.columnconfigure(i%3, weight=1)
            tk.Label(card, text=label, bg=BG2, fg=MUTED,
                     font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
            var = tk.StringVar(value="0")
            tk.Label(card, textvariable=var, bg=BG2, fg=ACCENT,
                     font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=(0, 8))
            self.metric_vars[key] = var

        tk.Button(frame, text="Refresh", bg=ACCENT, fg="white",
                  font=("Segoe UI", 9), bd=0, padx=12, pady=6,
                  command=self.load_metrics).pack(anchor="w", padx=10, pady=(0, 6))

        self.history_text = scrolledtext.ScrolledText(frame, bg=BG3, fg=TEXT,
                                                        font=("Consolas", 8), bd=0, padx=8, pady=8)
        self.history_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_health_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["health"] = frame
        tk.Button(frame, text="Run Health Check", bg=ACCENT, fg="white",
                  font=("Segoe UI", 9), bd=0, padx=14, pady=7,
                  command=self.load_health).pack(anchor="w", padx=10, pady=10)
        self.health_text = scrolledtext.ScrolledText(frame, bg=BG3, fg=TEXT,
                                                       font=("Consolas", 8), bd=0, padx=8, pady=8)
        self.health_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_files_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["files"] = frame

        tk.Button(frame, text="Refresh", bg=ACCENT, fg="white",
                  font=("Segoe UI", 9), bd=0, padx=12, pady=6,
                  command=self.load_workspaces).pack(anchor="w", padx=10, pady=8)

        paned = tk.PanedWindow(frame, orient="horizontal", bg=BG, bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left = tk.Frame(paned, bg=BG2)
        paned.add(left, width=320)

        self.ws_tree = ttk.Treeview(left, show="tree", selectmode="browse")
        self.ws_tree.pack(fill="both", expand=True)
        self.ws_tree.bind("<<TreeviewSelect>>", self._on_file_select)
        self.ws_tree.bind("<Double-Button-1>", self._on_file_double)

        style = ttk.Style()
        style.configure("Treeview", background=BG2, foreground=TEXT,
                         fieldbackground=BG2, borderwidth=0)
        style.configure("Treeview.Heading", background=BG2, foreground=ACCENT)
        style.map("Treeview", background=[("selected", "#30305a")])

        right = tk.Frame(paned, bg=BG3)
        paned.add(right)

        btn_row = tk.Frame(right, bg=BG3)
        btn_row.pack(fill="x", pady=4, padx=4)
        self.launch_btn = tk.Button(btn_row, text="▶ Run Selected File", bg=GREEN,
                                     fg="white", font=("Segoe UI", 9), bd=0, padx=10, pady=5,
                                     cursor="hand2", command=self._launch_selected,
                                     state="disabled")
        self.launch_btn.pack(side="left", padx=2)
        self.selected_file_path = None

        self.file_preview = scrolledtext.ScrolledText(right, bg=BG3, fg="#bbb",
                                                        font=("Consolas", 8), bd=0, padx=8, pady=4)
        self.file_preview.pack(fill="both", expand=True)
        self._file_path_map = {}

    def _build_memory_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["memory"] = frame

        top = tk.Frame(frame, bg=BG)
        top.pack(fill="x", padx=10, pady=8)
        self.mem_search = tk.Entry(top, bg=BG2, fg=TEXT, font=("Segoe UI", 9), bd=0,
                                    insertbackground=ACCENT, highlightthickness=1,
                                    highlightcolor=ACCENT, highlightbackground=BORDER)
        self.mem_search.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self.mem_search.bind("<Return>", lambda e: self.search_memory())
        tk.Button(top, text="Search", bg=ACCENT, fg="white", font=("Segoe UI", 9),
                  bd=0, padx=10, pady=6, command=self.search_memory).pack(side="left")
        tk.Button(top, text="All", bg=BG2, fg="#ccc", font=("Segoe UI", 9),
                  bd=0, padx=10, pady=6, command=self.load_memory).pack(side="left", padx=(4, 0))

        store_row = tk.Frame(frame, bg=BG)
        store_row.pack(fill="x", padx=10, pady=(0, 8))
        self.mem_key = tk.Entry(store_row, bg=BG2, fg=TEXT, font=("Segoe UI", 9),
                                 bd=0, insertbackground=ACCENT, highlightthickness=1,
                                 highlightcolor=ACCENT, highlightbackground=BORDER, width=20)
        self.mem_key.pack(side="left", ipady=6, padx=(0, 4))
        self.mem_val = tk.Entry(store_row, bg=BG2, fg=TEXT, font=("Segoe UI", 9),
                                 bd=0, insertbackground=ACCENT, highlightthickness=1,
                                 highlightcolor=ACCENT, highlightbackground=BORDER)
        self.mem_val.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self.mem_val.bind("<Return>", lambda e: self.store_memory())
        tk.Button(store_row, text="Store", bg=ACCENT, fg="white", font=("Segoe UI", 9),
                  bd=0, padx=10, pady=6, command=self.store_memory).pack(side="left")

        self.memory_text = scrolledtext.ScrolledText(frame, bg=BG3, fg=TEXT,
                                                       font=("Consolas", 8), bd=0, padx=8, pady=8)
        self.memory_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_settings_tab(self):
        frame = tk.Frame(self.tab_frame, bg=BG)
        self.tabs["settings"] = frame

        inner = tk.Frame(frame, bg=BG)
        inner.pack(fill="both", padx=20, pady=14)

        tk.Label(inner, text="LLM Provider", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 3))
        self.cfg_provider = ttk.Combobox(inner, values=["ollama", "groq", "openai", "anthropic"],
                                          state="readonly", width=40)
        self.cfg_provider.pack(anchor="w")
        self.cfg_provider.set("ollama")

        tk.Label(inner, text="Model", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 3))
        self.cfg_model = ttk.Combobox(inner, values=["qwen2.5-coder:14b", "llama3", "llama3.2"],
                                       state="normal", width=40)
        self.cfg_model.pack(anchor="w")
        self.cfg_model.set("qwen2.5-coder:14b")

        tk.Label(inner, text="API Key (Groq/OpenAI/Anthropic)", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 3))
        self.cfg_key = tk.Entry(inner, show="*", bg=BG2, fg=TEXT, font=("Segoe UI", 9),
                                 bd=0, insertbackground=ACCENT, highlightthickness=1,
                                 highlightcolor=ACCENT, highlightbackground=BORDER, width=44)
        self.cfg_key.pack(anchor="w", ipady=6)

        btn_row = tk.Frame(inner, bg=BG)
        btn_row.pack(anchor="w", pady=12)
        tk.Button(btn_row, text="Save Config", bg=ACCENT, fg="white",
                  font=("Segoe UI", 9), bd=0, padx=14, pady=7,
                  command=self.save_config).pack(side="left")
        self.cfg_msg = tk.Label(btn_row, text="", bg=BG, fg=GREEN, font=("Segoe UI", 9))
        self.cfg_msg.pack(side="left", padx=10)

        tk.Label(inner, text="Available Ollama Models", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 3))
        self.ollama_models_label = tk.Label(inner, text="Checking...", bg=BG, fg=MUTED,
                                             font=("Segoe UI", 8))
        self.ollama_models_label.pack(anchor="w")

        self.load_settings()

    def switch_tab(self, name):
        for n, frame in self.tabs.items():
            frame.pack_forget()
        for n, btn in self.tab_buttons.items():
            btn.configure(fg=MUTED, bg=BG2)
        self.tabs[name].pack(fill="both", expand=True)
        self.tab_buttons[name].configure(fg=ACCENT, bg="#1a1a3a")
        self.current_tab = name
        if name == "metrics":
            threading.Thread(target=self.load_metrics, daemon=True).start()
        if name == "files":
            threading.Thread(target=self.load_workspaces, daemon=True).start()
        if name == "memory":
            threading.Thread(target=self.load_memory, daemon=True).start()
        if name == "settings":
            threading.Thread(target=self.load_settings, daemon=True).start()

    def _chat_msg(self, text, tag="umbra"):
        self.chat_output.configure(state="normal")
        if tag == "user":
            self.chat_output.insert("end", "you > ", "user")
            self.chat_output.insert("end", text + "\n", "user")
        elif tag == "umbra":
            self.chat_output.insert("end", "umbra > ", tag)
            self.chat_output.insert("end", text + "\n", "umbra")
        else:
            self.chat_output.insert("end", text + "\n", tag)
        self.chat_output.configure(state="disabled")
        self.chat_output.see("end")

    def send_prompt(self):
        if not self.runtime_ready:
            self._chat_msg("Umbra is still loading. Please wait a few seconds.", "system")
            return
        prompt = self.chat_input.get().strip()
        if not prompt:
            return
        self.chat_input.delete(0, "end")
        self._chat_msg(prompt, "user")
        self.run_btn.configure(state="disabled", text="Running...")

        def do_run():
            try:
                run = self.runtime["pipeline"].run(prompt)
                self.runtime["monitor"].record(run)
                self.runtime["memory"].store(
                    f"run:{run.run_id}",
                    {"prompt": prompt, "status": run.status, "files": len(run.written_files)},
                    tags=["run", run.status],
                )
                # Auto-assemble
                assembled = self._auto_assemble(run, prompt)

                def update_ui():
                    status_c = "success" if run.status == "completed" else "umbra"
                    self._chat_msg(
                        f"Done! Status: {run.status} | Run: {run.run_id} | Tasks: {len(run.tasks)}",
                        status_c
                    )
                    if run.written_files:
                        self._chat_msg(f"Files written ({len(run.written_files)}):", "umbra")
                        for f in run.written_files:
                            self._chat_msg(f"  -> {f['file']} ({f['lines']} lines)", "file")
                    if assembled:
                        self._chat_msg(f"Assembled: {assembled}", "success")
                        self._chat_msg("Go to Files tab to preview and launch.", "system")
                    failed = [r for r in run.results if not r.success]
                    if failed:
                        self._chat_msg(f"Failed tasks: {len(failed)}", "error")
                    self.run_btn.configure(state="normal", text="Run")
                    self._update_sidebar()

                self.root.after(0, update_ui)
            except Exception as e:
                self.root.after(0, lambda: (
                    self._chat_msg(f"ERROR: {e}", "error"),
                    self.run_btn.configure(state="normal", text="Run")
                ))

        threading.Thread(target=do_run, daemon=True).start()

    def _auto_assemble(self, run, prompt):
        try:
            ws_base = os.path.join(_UMBRA_ROOT, "workspaces", run.run_id, "code")
            if not os.path.exists(ws_base):
                return None
            py_files = sorted([f for f in os.listdir(ws_base)
                                if f.endswith(".py") and "task_" in f])
            for fname in py_files:
                fpath = os.path.join(ws_base, fname)
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                if "pygame.init()" in content and "while" in content:
                    game_path = os.path.join(ws_base, "game.py")
                    with open(game_path, "w") as out:
                        out.write(content)
                    return game_path
                if "if __name__" in content and "main()" in content:
                    app_path = os.path.join(ws_base, "app.py")
                    if not os.path.exists(app_path):
                        with open(app_path, "w") as out:
                            out.write(content)
                    return app_path
            if py_files:
                best = max([os.path.join(ws_base, f) for f in py_files],
                           key=lambda p: os.path.getsize(p))
                main_path = os.path.join(ws_base, "main.py")
                if not os.path.exists(main_path):
                    import shutil
                    shutil.copy(best, main_path)
                    return main_path
        except Exception:
            pass
        return None

    def clear_chat(self):
        self.chat_output.configure(state="normal")
        self.chat_output.delete("1.0", "end")
        self.chat_output.configure(state="disabled")
        self._chat_msg("Chat cleared.", "system")

    def load_metrics(self):
        if not self.runtime_ready:
            return
        try:
            m = self.runtime["monitor"].get_summary()
            self.metric_vars["total"].set(str(m.get("total_runs", 0)))
            self.metric_vars["ok"].set(str(m.get("successful_runs", 0)))
            self.metric_vars["rate"].set(str(m.get("success_rate_pct", 0)) + "%")
            self.metric_vars["files"].set(str(m.get("total_files_written", 0)))
            self.metric_vars["tasks"].set(str(m.get("total_tasks_executed", 0)))
            self.metric_vars["dur"].set(str(m.get("avg_duration_seconds", 0)) + "s")

            runs = self.runtime["pipeline"].get_run_history()
            self.history_text.configure(state="normal")
            self.history_text.delete("1.0", "end")
            for r in reversed(runs):
                files = len(r.get("written_files", []))
                line = f"{r['run_id']} | {r['status']} | {files} files | {r['prompt'][:60]}\n"
                self.history_text.insert("end", line)
            self.history_text.configure(state="disabled")
        except Exception:
            pass

    def load_health(self):
        if not self.runtime_ready:
            return

        def do():
            try:
                report = self.runtime["health"].run_all_checks()
                d = report.to_dict()
                self.root.after(0, lambda: self._show_health(d))
            except Exception as e:
                self.root.after(0, lambda: self._show_health({"error": str(e)}))

        threading.Thread(target=do, daemon=True).start()

    def _show_health(self, d):
        self.health_text.configure(state="normal")
        self.health_text.delete("1.0", "end")
        if "error" in d:
            self.health_text.insert("end", "Error: " + d["error"])
        else:
            self.health_text.insert("end",
                f"Overall: {d['overall_status'].upper()} | "
                f"Pass: {d['pass_count']} Warn: {d['warn_count']} Fail: {d['fail_count']}\n\n")
            for c in d.get("checks", []):
                icon = "✓" if c["status"] == "pass" else ("!" if c["status"] == "warn" else "✗")
                self.health_text.insert("end",
                    f"  {icon} {c['name']}: {c.get('message', c['status'])}\n")
        self.health_text.configure(state="disabled")

    def load_workspaces(self):
        ws_dir = os.path.join(_UMBRA_ROOT, "workspaces")
        self.ws_tree.delete(*self.ws_tree.get_children())
        self._file_path_map.clear()
        if not os.path.exists(ws_dir):
            return
        for d in sorted(os.listdir(ws_dir), reverse=True)[:20]:
            ws_path = os.path.join(ws_dir, d)
            if not os.path.isdir(ws_path):
                continue
            code_dir = os.path.join(ws_path, "code")
            parent = self.ws_tree.insert("", "end", text=f"📁 {d}", open=False)
            if os.path.exists(code_dir):
                for f in sorted(os.listdir(code_dir)):
                    if f.endswith((".py", ".md", ".json")):
                        fp = os.path.join(code_dir, f)
                        icon = "▶ " if f.endswith(".py") else "  "
                        item = self.ws_tree.insert(parent, "end", text=f"{icon}{f}")
                        self._file_path_map[item] = fp

    def _on_file_select(self, event):
        sel = self.ws_tree.selection()
        if not sel:
            return
        item = sel[0]
        path = self._file_path_map.get(item)
        if path and os.path.exists(path):
            self.selected_file_path = path
            self.launch_btn.configure(state="normal" if path.endswith(".py") else "disabled")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                self.file_preview.configure(state="normal")
                self.file_preview.delete("1.0", "end")
                self.file_preview.insert("1.0", content)
                self.file_preview.configure(state="disabled")
            except Exception:
                pass

    def _on_file_double(self, event):
        self._launch_selected()

    def _launch_selected(self):
        if not self.selected_file_path:
            return
        path = self.selected_file_path
        if not path.endswith(".py"):
            return
        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    [sys.executable, path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    cwd=os.path.dirname(path),
                )
            else:
                subprocess.Popen([sys.executable, path], cwd=os.path.dirname(path))
            self._chat_msg(f"Launched: {os.path.basename(path)}", "success")
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))

    def load_memory(self):
        if not self.runtime_ready:
            return
        try:
            mem = self.runtime["memory"]
            keys = mem.list_keys()[:50]
            self.memory_text.configure(state="normal")
            self.memory_text.delete("1.0", "end")
            if not keys:
                self.memory_text.insert("end", "No memory entries yet.\n")
            for k in keys:
                self.memory_text.insert("end", f"{k}\n")
            self.memory_text.configure(state="disabled")
        except Exception:
            pass

    def search_memory(self):
        if not self.runtime_ready:
            return
        q = self.mem_search.get().strip()
        if not q:
            return
        try:
            results = self.runtime["memory"].search(q, top_k=10)
            self.memory_text.configure(state="normal")
            self.memory_text.delete("1.0", "end")
            if not results:
                self.memory_text.insert("end", f"Nothing found for '{q}'\n")
            for r in results:
                self.memory_text.insert("end", f"{r.key}: {str(r.value)[:100]}\n")
            self.memory_text.configure(state="disabled")
        except Exception:
            pass

    def store_memory(self):
        if not self.runtime_ready:
            return
        key = self.mem_key.get().strip() or None
        val = self.mem_val.get().strip()
        if not val:
            return
        try:
            self.runtime["memory"].store(key or f"note:{datetime.now().isoformat()}", val, tags=["user_note"])
            self.runtime["memory"].save()
            self.mem_key.delete(0, "end")
            self.mem_val.delete(0, "end")
            self.load_memory()
        except Exception:
            pass

    def load_settings(self):
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as resp:
                data = json.loads(resp.read())
                models = [m["name"] for m in data.get("models", [])]
                if models:
                    self.root.after(0, lambda: (
                        self.cfg_model.configure(values=models),
                        self.ollama_models_label.configure(text=", ".join(models))
                    ))
        except Exception:
            self.root.after(0, lambda: self.ollama_models_label.configure(text="Ollama not reachable"))
        if self.runtime_ready:
            cfg = self.runtime["config"].to_dict()
            self.root.after(0, lambda: (
                self.cfg_provider.set(cfg.get("llm_provider", "ollama")),
                self.cfg_model.set(cfg.get("llm_model", "qwen2.5-coder:14b"))
            ))

    def save_config(self):
        if not self.runtime_ready:
            return
        cfg = {
            "llm_provider": self.cfg_provider.get(),
            "llm_model": self.cfg_model.get(),
        }
        key = self.cfg_key.get().strip()
        if key:
            cfg["llm_api_key"] = key
        for k, v in cfg.items():
            self.runtime["config"].set(k, v)
        self.runtime["config"].save()
        self.cfg_msg.configure(text="Saved!")
        self.root.after(2000, lambda: self.cfg_msg.configure(text=""))

    def do_health(self):
        self.switch_tab("health")
        self.load_health()

    def do_validate(self):
        if not self.runtime_ready:
            return
        last = self.runtime["pipeline"].get_last_run()
        if not last or not last.written_files:
            self._chat_msg("No recent run with files to validate.", "system")
            return
        ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
        result = self.runtime["run_validator"].validate_run(last, workspace_base=ws_base)
        color = "success" if result.passed else "error"
        self._chat_msg(f"Validation: {result.score}/100 | Passed: {result.passed}", color)
        self.switch_tab("chat")

    def do_review(self):
        if not self.runtime_ready:
            return
        last = self.runtime["pipeline"].get_last_run()
        if not last or not last.written_files:
            self._chat_msg("No recent run with files to review.", "system")
            return
        ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
        reviews = self.runtime["reviewer"].review_pipeline_run(last, workspace_base=ws_base)
        avg = self.runtime["reviewer"].get_aggregate_score(reviews)
        self._chat_msg(f"Code review: {len(reviews)} files | Avg score: {avg}/100", "success")
        self.switch_tab("chat")

    def _update_sidebar(self):
        if not self.runtime_ready:
            return
        try:
            llm = self.runtime["llm"]
            self.stat_provider.set(llm.get_provider() + (" (FREE)" if llm.is_free() else ""))
            self.stat_model.set(llm.get_model())
            runs = self.runtime["pipeline"].get_run_history()
            self.stat_runs.set(str(len(runs)))
            self.stat_memory.set(str(self.runtime["memory"].size()) + " entries")
            rm = self.runtime.get("resource_manager")
            if rm:
                rs = rm.get_current_status()
                self.stat_ram.set(str(rs.get("memory_pct", 0)) + "%")
                if rs.get("gaming_detected"):
                    self.gaming_frame.pack(padx=10, pady=4, fill="x")
                    self.status_label.configure(text="● GAMING MODE", fg=ORANGE)
                else:
                    self.gaming_frame.pack_forget()
                    self.status_label.configure(text="● Ready", fg=GREEN)
        except Exception:
            pass

    def _update_status_bar_loop(self):
        self._update_sidebar()
        self.root.after(15000, self._update_status_bar_loop)

    def _start_runtime(self):
        def build():
            try:
                from umbra import build_runtime
                self.runtime = build_runtime()
                self.runtime_ready = True
                self.root.after(0, self._on_runtime_ready)
            except Exception as e:
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"● Error: {str(e)[:40]}", fg=RED))

        threading.Thread(target=build, daemon=True).start()

    def _on_runtime_ready(self):
        self.status_label.configure(text="● Ready", fg=GREEN)
        llm = self.runtime["llm"]
        self.model_label.configure(text=f"{llm.get_provider()} / {llm.get_model()}")
        self._update_sidebar()
        self.load_workspaces()
        self._chat_msg(f"Runtime ready! Using {llm.get_provider()} / {llm.get_model()}", "success")


def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    app = UmbraDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()