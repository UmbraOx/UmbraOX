# C:\Umbra\core\gui\control_center.py
# C:\Umbra\core\ui\umbra_control_center.py  (copy to both)
# Umbra Control Center v3.0 - Full working GUI
# All output from _umbra_print() routes here via post_message()
# Tabs: Console, Task Queue, Files, Image/Video Preview, Agents, Memory

import os, sys, json, time, queue, threading, subprocess, importlib
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

C = {
    "bg":      "#0d0d1a", "panel":  "#13132a", "border": "#2a2a5a",
    "accent":  "#6a40d4", "accent2":"#4060c0", "green":  "#30c060",
    "red":     "#c03040", "yellow": "#c0a020", "text":   "#d0d0e8",
    "dim":     "#707090", "input":  "#1a1a30", "btn":    "#2a2a50",
    "log":     "#0a0a18", "logtext":"#a0c0a0",
}
FM = ("Consolas", 11)
FL = ("Segoe UI", 10)
FT = ("Segoe UI", 13, "bold")
FS = ("Consolas", 9)


class UmbraControlCenter(tk.Tk):
    def __init__(self, runtime=None, process_fn=None):
        super().__init__()
        self.runtime    = runtime
        self.process_fn = process_fn
        self._q         = queue.Queue()   # thread-safe output queue
        self._history   = []
        self._hist_idx  = 0
        self._ws        = os.path.join(_ROOT, "workspaces")
        self._jobs      = []  # task queue items
        self._job_id    = 0
        self._setup_window()
        self._build_ui()
        self._start_drain()
        self.log("[UMBRA] Control Center v3.0 ready.", C["green"])
        self.log("[UMBRA] Type commands below or use the sidebar.", C["dim"])

    def _setup_window(self):
        self.title("UMBRA — Autonomous AI Runtime OS v2.4.0")
        self.configure(bg=C["bg"])
        self.geometry("1400x860")
        self.minsize(1000, 600)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        try:
            self.iconbitmap(os.path.join(_ROOT, "core", "assets", "umbra.ico"))
        except Exception:
            pass

    def _build_ui(self):
        # Title bar
        tb = tk.Frame(self, bg=C["panel"], height=50)
        tb.pack(fill=tk.X)
        tb.pack_propagate(False)
        tk.Label(tb, text="⬡  UMBRA", font=FT, fg=C["accent"], bg=C["panel"]).pack(side=tk.LEFT, padx=16, pady=12)
        tk.Label(tb, text="Autonomous AI Runtime OS", font=FL, fg=C["dim"], bg=C["panel"]).pack(side=tk.LEFT)
        self._status_lbl = tk.Label(tb, text="● READY", font=FL, fg=C["green"], bg=C["panel"])
        self._status_lbl.pack(side=tk.RIGHT, padx=16)

        # Progress bar (hidden until task runs)
        self._prog_frame = tk.Frame(self, bg=C["panel"], height=6)
        self._prog_frame.pack(fill=tk.X)
        self._prog = ttk.Progressbar(self._prog_frame, mode="indeterminate", length=400)
        # Don't pack yet - shown during tasks

        # Main layout
        pw = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=C["bg"], sashwidth=5)
        pw.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Sidebar
        left = tk.Frame(pw, bg=C["panel"], width=200)
        pw.add(left, minsize=180)
        self._build_sidebar(left)

        # Notebook
        right = tk.Frame(pw, bg=C["bg"])
        pw.add(right, minsize=700)
        self._build_tabs(right)

    def _build_sidebar(self, p):
        tk.Label(p, text="QUICK ACTIONS", font=FS, fg=C["dim"], bg=C["panel"]).pack(pady=(12,4), padx=8, anchor="w")
        actions = [
            ("📊 Status",              "status"),
            ("🔧 Fix All Bugs",        "fix all bugs"),
            ("🎮 Build Game",          "make a game called MyGame"),
            ("🖼 Make Image",          "make an image of a fantasy landscape"),
            ("🎬 Make GIF",            "make a gif of a dragon flying"),
            ("📁 List Files",          "list files"),
            ("🧹 Clean Old Files",     "clean up old files"),
            ("💾 List Projects",       "projects"),
            ("📋 Help",                "help"),
            ("▶ Play Last Game",       "play last"),
        ]
        for lbl, cmd in actions:
            tk.Button(p, text=lbl, font=FS, fg=C["text"], bg=C["btn"],
                      activebackground="#3a3a70", activeforeground=C["text"],
                      relief=tk.FLAT, cursor="hand2", anchor="w", padx=10,
                      command=lambda c=cmd: self._quick(c)).pack(fill=tk.X, padx=6, pady=2)

        tk.Frame(p, bg=C["border"], height=1).pack(fill=tk.X, padx=8, pady=8)
        tk.Label(p, text="SYSTEM", font=FS, fg=C["dim"], bg=C["panel"]).pack(padx=8, anchor="w")
        tk.Button(p, text="✖ Close Umbra", font=FS, fg=C["text"], bg=C["btn"],
                  activebackground="#3a3a70", activeforeground=C["text"],
                  relief=tk.FLAT, cursor="hand2", anchor="w", padx=10,
                  command=self._on_close).pack(fill=tk.X, padx=6, pady=2)

        tk.Frame(p, bg=C["border"], height=1).pack(fill=tk.X, padx=8, pady=8)
        self._side_info = tk.Label(p, text="Ollama: checking...\nComfyUI: offline",
                                   font=FS, fg=C["dim"], bg=C["panel"],
                                   justify=tk.LEFT, wraplength=180)
        self._side_info.pack(padx=8, anchor="w")
        self.after(2000, self._update_side_info)

    def _build_tabs(self, p):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=C["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=C["btn"], foreground=C["dim"],
                        font=FL, padding=[10,5])
        style.map("TNotebook.Tab",
                  background=[("selected", C["accent"])],
                  foreground=[("selected","#ffffff")])
        self._nb = ttk.Notebook(p)
        self._nb.pack(fill=tk.BOTH, expand=True)

        self._tc = tk.Frame(self._nb, bg=C["bg"])
        self._tq = tk.Frame(self._nb, bg=C["bg"])
        self._tf = tk.Frame(self._nb, bg=C["bg"])
        self._tp = tk.Frame(self._nb, bg=C["bg"])
        self._ta = tk.Frame(self._nb, bg=C["bg"])
        self._tm = tk.Frame(self._nb, bg=C["bg"])

        self._nb.add(self._tc, text="  💬 Console  ")
        self._nb.add(self._tq, text="  📋 Task Queue  ")
        self._nb.add(self._tf, text="  📁 Files  ")
        self._nb.add(self._tp, text="  🖼 Preview  ")
        self._nb.add(self._ta, text="  🤖 Agents  ")
        self._nb.add(self._tm, text="  🧠 Memory  ")

        self._build_console(self._tc)
        self._build_taskqueue(self._tq)
        self._build_files(self._tf)
        self._build_preview(self._tp)
        self._build_agents(self._ta)
        self._build_memory(self._tm)

    # ── CONSOLE TAB ──────────────────────────────────────────────────────────
    def _build_console(self, p):
        self._out = scrolledtext.ScrolledText(
            p, bg=C["log"], fg=C["logtext"], font=FM, wrap=tk.WORD,
            state=tk.DISABLED, relief=tk.FLAT, bd=0, insertbackground=C["text"])
        self._out.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        for tag, col in [("green",C["green"]),("red",C["red"]),("yellow",C["yellow"]),
                         ("accent",C["accent"]),("dim",C["dim"]),("white",C["text"])]:
            self._out.tag_config(tag, foreground=col)

        inp = tk.Frame(p, bg=C["panel"], pady=6)
        inp.pack(fill=tk.X, padx=6, pady=(0,6))
        tk.Label(inp, text="umbra >", font=FM, fg=C["accent"], bg=C["panel"]).pack(side=tk.LEFT, padx=(8,4))
        self._entry = tk.Entry(inp, bg=C["input"], fg=C["text"], font=FM, relief=tk.FLAT,
                               insertbackground=C["text"],
                               highlightthickness=1, highlightbackground=C["border"],
                               highlightcolor=C["accent"])
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        self._entry.bind("<Return>", self._on_enter)
        self._entry.bind("<Up>",    self._hist_up)
        self._entry.bind("<Down>",  self._hist_dn)
        self._entry.focus_set()
        tk.Button(inp, text="Send ▶", font=FL, fg="#fff", bg=C["accent"],
                  activebackground=C["accent2"], relief=tk.FLAT, padx=12,
                  cursor="hand2", command=self._on_enter).pack(side=tk.RIGHT, padx=(4,8))

    # ── TASK QUEUE TAB ────────────────────────────────────────────────────────
    def _build_taskqueue(self, p):
        tk.Label(p, text="Active & Queued Tasks", font=FL, fg=C["dim"], bg=C["bg"]).pack(pady=8, padx=10, anchor="w")

        bar = tk.Frame(p, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0,4))
        tk.Button(bar, text="🔄 Refresh", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._refresh_jobs).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="⬆ Priority Up", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._job_up).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="⬇ Priority Down", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._job_dn).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="🗑 Remove", font=FS, fg=C["red"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._job_remove).pack(side=tk.LEFT, padx=2)

        cols = ("ID","Task","Type","Status","Priority")
        self._job_tree = ttk.Treeview(p, columns=cols, show="headings", height=22)
        self._job_tree.heading("ID",       text="ID");       self._job_tree.column("ID",       width=50)
        self._job_tree.heading("Task",     text="Task");     self._job_tree.column("Task",     width=350)
        self._job_tree.heading("Type",     text="Type");     self._job_tree.column("Type",     width=100)
        self._job_tree.heading("Status",   text="Status");   self._job_tree.column("Status",   width=100)
        self._job_tree.heading("Priority", text="Priority"); self._job_tree.column("Priority", width=80)
        sb = ttk.Scrollbar(p, orient=tk.VERTICAL, command=self._job_tree.yview)
        self._job_tree.configure(yscrollcommand=sb.set)
        self._job_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=4)
        sb.pack(side=tk.LEFT, fill=tk.Y, pady=4)

    def _refresh_jobs(self):
        for i in self._job_tree.get_children(): self._job_tree.delete(i)
        for j in self._jobs:
            self._job_tree.insert("", tk.END, values=(
                j["id"], j["task"][:60], j["type"], j["status"], j["priority"]))

    def _job_up(self):
        sel = self._job_tree.selection()
        if not sel: return
        vals = self._job_tree.item(sel[0])["values"]
        jid  = vals[0]
        for j in self._jobs:
            if j["id"] == jid:
                j["priority"] = min(10, j["priority"]+1)
        self._jobs.sort(key=lambda x: -x["priority"])
        self._refresh_jobs()

    def _job_dn(self):
        sel = self._job_tree.selection()
        if not sel: return
        vals = self._job_tree.item(sel[0])["values"]
        jid  = vals[0]
        for j in self._jobs:
            if j["id"] == jid:
                j["priority"] = max(1, j["priority"]-1)
        self._jobs.sort(key=lambda x: -x["priority"])
        self._refresh_jobs()

    def _job_remove(self):
        sel = self._job_tree.selection()
        if not sel: return
        vals = self._job_tree.item(sel[0])["values"]
        jid  = vals[0]
        self._jobs = [j for j in self._jobs if j["id"] != jid]
        self._refresh_jobs()

    def add_job(self, task, task_type="general", status="queued", priority=5):
        self._job_id += 1
        self._jobs.append({"id": self._job_id, "task": task, "type": task_type,
                            "status": status, "priority": priority})
        self._jobs.sort(key=lambda x: -x["priority"])
        self.after(0, self._refresh_jobs)

    def update_job_status(self, task, status):
        for j in self._jobs:
            if j["task"] == task or task in j["task"]:
                j["status"] = status
        self.after(0, self._refresh_jobs)

    # ── FILES TAB ─────────────────────────────────────────────────────────────
    def _build_files(self, p):
        tk.Label(p, text="Workspace Files", font=FL, fg=C["dim"], bg=C["bg"]).pack(pady=8, padx=10, anchor="w")
        bar = tk.Frame(p, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0,4))
        tk.Button(bar, text="🔄 Refresh",    font=FS, fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=8, command=self._refresh_files).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="📂 Open Folder",font=FS, fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=8, command=self._open_ws).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="▶ Run",         font=FS, fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=8, command=self._run_sel).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="🖼 Preview",    font=FS, fg=C["text"], bg=C["btn"], relief=tk.FLAT, padx=8, command=self._preview_sel).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="🗑 Delete",     font=FS, fg=C["red"],  bg=C["btn"], relief=tk.FLAT, padx=8, command=self._del_sel).pack(side=tk.LEFT, padx=2)

        cols = ("Name","Size","Modified","Type")
        self._ft = ttk.Treeview(p, columns=cols, show="headings", height=22)
        self._ft.heading("Name",     text="Name");     self._ft.column("Name",     width=300)
        self._ft.heading("Size",     text="Size");     self._ft.column("Size",     width=80)
        self._ft.heading("Modified", text="Modified"); self._ft.column("Modified", width=150)
        self._ft.heading("Type",     text="Type");     self._ft.column("Type",     width=80)
        sb2 = ttk.Scrollbar(p, orient=tk.VERTICAL, command=self._ft.yview)
        self._ft.configure(yscrollcommand=sb2.set)
        self._ft.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=4)
        sb2.pack(side=tk.LEFT, fill=tk.Y, pady=4)
        self._ft.bind("<Double-1>", lambda e: self._run_sel())
        self._refresh_files()

    def _refresh_files(self):
        for i in self._ft.get_children(): self._ft.delete(i)
        if not os.path.isdir(self._ws): return
        for root, dirs, files in os.walk(self._ws):
            dirs[:] = [d for d in dirs if d not in ("__pycache__",".git")]
            level   = root.replace(self._ws,"").count(os.sep)
            if level > 3: continue
            rel = os.path.relpath(root, self._ws)
            if rel != ".":
                self._ft.insert("","end", values=("📁 "+rel+"/","","","folder"), tags=("",))
            for fn in sorted(files)[:30]:
                fp = os.path.join(root, fn)
                try:
                    sz  = os.path.getsize(fp)
                    mod = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(fp)))
                    ext = os.path.splitext(fn)[1]
                    szs = f"{sz//1024}KB" if sz>1024 else f"{sz}B"
                    self._ft.insert("","end", values=(fn,szs,mod,ext), tags=(fp,))
                except Exception:
                    pass

    def _open_ws(self):
        os.makedirs(self._ws, exist_ok=True)
        if sys.platform=="win32": os.startfile(self._ws)
        else: subprocess.Popen(["xdg-open", self._ws])

    def _get_sel_path(self):
        sel = self._ft.selection()
        if not sel: return None
        tags = self._ft.item(sel[0], "tags")
        return tags[0] if tags and tags[0] and os.path.isfile(tags[0]) else None

    def _run_sel(self):
        fp = self._get_sel_path()
        if fp and fp.endswith(".py"):
            subprocess.Popen([sys.executable, fp], cwd=os.path.dirname(fp))
            self.log(f"[GUI] Launched: {fp}", C["green"])

    def _preview_sel(self):
        fp = self._get_sel_path()
        if not fp: return
        ext = os.path.splitext(fp)[1].lower()
        if ext in (".png",".jpg",".jpeg",".gif",".bmp"):
            self._show_image_preview(fp)
            self._nb.select(self._tp)  # Switch to preview tab
        elif ext == ".py":
            self._run_sel()

    def _del_sel(self):
        fp = self._get_sel_path()
        if not fp: return
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(fp)}?"):
            try: os.remove(fp); self.log(f"[GUI] Deleted: {fp}", C["yellow"]); self._refresh_files()
            except Exception as e: self.log(f"[GUI] Error: {e}", C["red"])

    # ── PREVIEW TAB ──────────────────────────────────────────────────────────
    def _build_preview(self, p):
        tk.Label(p, text="Image / Video Preview", font=FL, fg=C["dim"], bg=C["bg"]).pack(pady=8, padx=10, anchor="w")
        bar = tk.Frame(p, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0,4))
        tk.Button(bar, text="📂 Browse Image", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._browse_image).pack(side=tk.LEFT, padx=2)
        tk.Button(bar, text="🔄 Refresh Latest", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._load_latest_image).pack(side=tk.LEFT, padx=2)

        self._prev_lbl = tk.Label(p, bg=C["bg"], text="No image loaded\n\nImages you generate will appear here.\nUse 'make an image of...' to generate one.",
                                  fg=C["dim"], font=FL, wraplength=600)
        self._prev_lbl.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self._prev_info = tk.Label(p, text="", fg=C["dim"], bg=C["bg"], font=FS)
        self._prev_info.pack(pady=4)

        # Gallery row
        gbar = tk.Frame(p, bg=C["bg"])
        gbar.pack(fill=tk.X, padx=10, pady=(0,8))
        tk.Label(gbar, text="Recent:", fg=C["dim"], bg=C["bg"], font=FS).pack(side=tk.LEFT, padx=4)
        self._gallery_frame = tk.Frame(gbar, bg=C["bg"])
        self._gallery_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _show_image_preview(self, path):
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            # Fit to ~700x500
            img.thumbnail((700, 500), Image.LANCZOS)
            self._prev_photo = ImageTk.PhotoImage(img)
            self._prev_lbl.configure(image=self._prev_photo, text="")
            size = os.path.getsize(path)
            self._prev_info.configure(text=f"{os.path.basename(path)}  |  {img.size[0]}x{img.size[1]}  |  {size//1024}KB")
        except ImportError:
            self._prev_lbl.configure(text=f"PIL not installed.\nInstall: pip install Pillow\n\nFile: {path}", image="")
        except Exception as e:
            self._prev_lbl.configure(text=f"Cannot preview: {e}", image="")

    def _browse_image(self):
        fp = filedialog.askopenfilename(
            title="Open Image", initialdir=os.path.join(self._ws,"images"),
            filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.bmp"),("All","*.*")])
        if fp: self._show_image_preview(fp)

    def _load_latest_image(self):
        img_dir = os.path.join(self._ws, "images")
        if not os.path.isdir(img_dir): return
        imgs = [(os.path.getmtime(os.path.join(img_dir,f)), os.path.join(img_dir,f))
                for f in os.listdir(img_dir) if f.lower().endswith((".png",".jpg",".jpeg",".gif"))]
        if imgs:
            imgs.sort(reverse=True)
            self._show_image_preview(imgs[0][1])
            self._nb.select(self._tp)

    # ── AGENTS TAB ────────────────────────────────────────────────────────────
    def _build_agents(self, p):
        tk.Label(p, text="Agent Status", font=FL, fg=C["dim"], bg=C["bg"]).pack(pady=8, padx=10, anchor="w")
        agents = [
            ("World Agent",      "Generates world map, biomes, towns, camps"),
            ("Character Agent",  "Player, Enemy, NPC classes and stats"),
            ("Item Agent",       "Weapons, armor, spells, loot tables"),
            ("Mechanic Agent",   "Combat, crafting, save/load systems"),
            ("UI Agent",         "HUD, menus, inventory, dialogue panels"),
            ("Quest Agent",      "Quest data, spawn logic, progression"),
            ("Economy Agent",    "Shops, crafting recipes, building costs"),
            ("Image Agent",      "ComfyUI image generation pipeline"),
            ("Sprite Agent",     "PIL pixel-art sprite generator"),
            ("GIF Agent",        "PIL animated GIF generator"),
            ("TTS Agent",        "Text-to-speech via pyttsx3"),
            ("Voice Agent",      "Speech recognition microphone input"),
            ("Code Agent",       "Ollama code generation pipeline"),
            ("Repair Agent",     "Syntax checking and auto-repair"),
        ]
        cols = ("Agent","Description","Status")
        self._ag_tree = ttk.Treeview(p, columns=cols, show="headings", height=18)
        self._ag_tree.heading("Agent",       text="Agent");       self._ag_tree.column("Agent",       width=160)
        self._ag_tree.heading("Description", text="Description"); self._ag_tree.column("Description", width=400)
        self._ag_tree.heading("Status",      text="Status");      self._ag_tree.column("Status",      width=100)
        for name, desc in agents:
            self._ag_tree.insert("","end", values=(name, desc, "standby"))
        sb3 = ttk.Scrollbar(p, orient=tk.VERTICAL, command=self._ag_tree.yview)
        self._ag_tree.configure(yscrollcommand=sb3.set)
        self._ag_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=4)
        sb3.pack(side=tk.LEFT, fill=tk.Y, pady=4)

    def update_agent_status(self, agent_name, status):
        """Called by Umbra when an agent starts/finishes."""
        for item in self._ag_tree.get_children():
            vals = self._ag_tree.item(item)["values"]
            if vals and agent_name.lower() in str(vals[0]).lower():
                self._ag_tree.item(item, values=(vals[0], vals[1], status))
                break

    # ── MEMORY TAB ────────────────────────────────────────────────────────────
    def _build_memory(self, p):
        tk.Label(p, text="Runtime Memory", font=FL, fg=C["dim"], bg=C["bg"]).pack(pady=8, padx=10, anchor="w")
        bar = tk.Frame(p, bg=C["bg"])
        bar.pack(fill=tk.X, padx=10, pady=(0,4))
        tk.Button(bar, text="🔄 Refresh", font=FS, fg=C["text"], bg=C["btn"],
                  relief=tk.FLAT, padx=8, command=self._refresh_mem).pack(side=tk.LEFT, padx=2)
        tk.Label(bar, text="Search:", fg=C["dim"], bg=C["bg"], font=FS).pack(side=tk.LEFT, padx=(10,4))
        self._mem_search = tk.Entry(bar, bg=C["input"], fg=C["text"], font=FS, width=30, relief=tk.FLAT)
        self._mem_search.pack(side=tk.LEFT)
        self._mem_search.bind("<Return>", lambda e: self._refresh_mem())

        cols = ("Key","Value","Tags")
        self._mem_tree = ttk.Treeview(p, columns=cols, show="headings", height=22)
        self._mem_tree.heading("Key",   text="Key");   self._mem_tree.column("Key",   width=200)
        self._mem_tree.heading("Value", text="Value"); self._mem_tree.column("Value", width=400)
        self._mem_tree.heading("Tags",  text="Tags");  self._mem_tree.column("Tags",  width=160)
        sb4 = ttk.Scrollbar(p, orient=tk.VERTICAL, command=self._mem_tree.yview)
        self._mem_tree.configure(yscrollcommand=sb4.set)
        self._mem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=4)
        sb4.pack(side=tk.LEFT, fill=tk.Y, pady=4)

    def _refresh_mem(self):
        for i in self._mem_tree.get_children(): self._mem_tree.delete(i)
        if not self.runtime: return
        mem = self.runtime.get("memory") if isinstance(self.runtime, dict) else getattr(self.runtime,"memory",None)
        if not mem: return
        query = self._mem_search.get().strip().lower()
        try:
            entries = mem.list_all() if hasattr(mem,"list_all") else []
            for e in entries:
                k = str(e.get("key",""));  v = str(e.get("value",""))[:120]; t = str(e.get("tags",""))
                if not query or query in k.lower() or query in v.lower():
                    self._mem_tree.insert("","end", values=(k,v,t))
        except Exception:
            pass

    # ── LOGGING ───────────────────────────────────────────────────────────────
    def log(self, msg, colour=None):
        """Thread-safe log. This IS post_message."""
        self._q.put((str(msg), colour))

    def post_message(self, text):
        """Called by _umbra_print() in Umbra.py"""
        self.log(text)

    def _write(self, msg, colour=None):
        self._out.configure(state=tk.NORMAL)
        ts  = time.strftime("%H:%M:%S")
        low = msg.lower()
        if colour:
            rev = {C["green"]:"green",C["red"]:"red",C["yellow"]:"yellow",C["accent"]:"accent",C["dim"]:"dim"}
            tag = rev.get(colour,"white")
        elif any(x in low for x in ("[error]","[fail]","failed","error:")):
            tag = "red"
        elif any(x in low for x in ("[ok]","[done]","[pass]","complete","saved","ready","built")):
            tag = "green"
        elif any(x in low for x in ("[warn]","warning","missing","offline")):
            tag = "yellow"
        elif any(x in low for x in ("[umbra]","[agent","[plan]","[build]","[stitch]","[syntax]","[test]","[deliver]")):
            tag = "accent"
        elif msg.startswith("  ") or msg.startswith("["):
            tag = "dim"
        else:
            tag = "white"
        self._out.insert(tk.END, f"[{ts}] {msg}\n", tag)
        self._out.see(tk.END)
        self._out.configure(state=tk.DISABLED)

    def _start_drain(self):
        self.after(50, self._drain)

    def _drain(self):
        try:
            while True:
                msg, col = self._q.get_nowait()
                self._write(msg, col)
        except queue.Empty:
            pass
        self.after(50, self._drain)

    # ── INPUT ─────────────────────────────────────────────────────────────────
    def _on_enter(self, event=None):
        text = self._entry.get().strip()
        if not text: return
        self._entry.delete(0, tk.END)
        if not self._history or self._history[-1] != text:
            self._history.append(text)
        self._hist_idx = len(self._history)
        self.log(f"[YOU] {text}", C["accent"])
        self._send(text)

    def _send(self, text):
        # Add to job queue display
        ttype = "game" if "game" in text.lower() else "image" if "image" in text.lower() else "general"
        self.add_job(text, ttype, "running")
        # Show progress
        self._prog.pack(fill=tk.X)
        self._prog.start(10)
        self._status_lbl.configure(text="● WORKING", fg=C["yellow"])

        def _run():
            try:
                if self.process_fn and self.runtime:
                    self.process_fn(self.runtime, text)
                elif self.runtime:
                    for attr in ("run_prompt","process","handle"):
                        fn = getattr(self.runtime, attr, None)
                        if fn: fn(text); break
                else:
                    self.log("[GUI] No runtime connected.", C["yellow"])
            except Exception as e:
                self.log(f"[ERROR] {e}", C["red"])
            finally:
                self.after(0, self._task_done)
                self.update_job_status(text, "done")

        threading.Thread(target=_run, daemon=True).start()

    def _task_done(self):
        self._prog.stop()
        self._prog.pack_forget()
        self._status_lbl.configure(text="● READY", fg=C["green"])
        # Auto-refresh files and check for new images
        self._refresh_files()
        self._load_latest_image()

    def _quick(self, cmd):
        self._entry.delete(0, tk.END)
        self._entry.insert(0, cmd)
        self._on_enter()

    def _hist_up(self, event=None):
        if not self._history: return
        self._hist_idx = max(0, self._hist_idx-1)
        self._entry.delete(0, tk.END)
        self._entry.insert(0, self._history[self._hist_idx])

    def _hist_dn(self, event=None):
        if not self._history: return
        self._hist_idx = min(len(self._history), self._hist_idx+1)
        self._entry.delete(0, tk.END)
        if self._hist_idx < len(self._history):
            self._entry.insert(0, self._history[self._hist_idx])

    # ── SIDEBAR INFO ──────────────────────────────────────────────────────────
    def _update_side_info(self):
        ollama = "online" if self._check_ollama() else "offline"
        comfy  = "online" if self._check_comfyui() else "offline"
        self._side_info.configure(text=f"Ollama: {ollama}\nComfyUI: {comfy}")
        self.after(10000, self._update_side_info)

    def _check_ollama(self):
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2).close()
            return True
        except Exception: return False

    def _check_comfyui(self):
        try:
            import urllib.request
            urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=2).close()
            return True
        except Exception: return False

    # ── CLOSE ─────────────────────────────────────────────────────────────────
    def _on_close(self):
        if messagebox.askyesno("Close Umbra", "Close Umbra completely?"):
            try: self.destroy()
            except Exception: pass
            import os as _os; _os._exit(0)


# ── LAUNCH FUNCTIONS ──────────────────────────────────────────────────────────

def launch_control_center(runtime=None, process_fn=None):
    """Launch on calling thread (must be main thread)."""
    app = UmbraControlCenter(runtime=runtime, process_fn=process_fn)
    app.mainloop()
    return app


def launch_in_thread(runtime=None, process_fn=None):
    """
    Returns the app instance immediately.
    Caller must run app.mainloop() on main thread.
    """
    app = UmbraControlCenter.__new__(UmbraControlCenter)
    # Just return a configured instance; Umbra.py calls gui.run() on main thread
    app._runtime    = runtime
    app._process_fn = process_fn
    # Actually build it properly
    app.__init__(runtime=runtime, process_fn=process_fn)
    return app


if __name__ == "__main__":
    app = UmbraControlCenter()
    app.log("Umbra Control Center — standalone test mode", app.C["green"] if hasattr(app,"C") else None)
    app.mainloop()