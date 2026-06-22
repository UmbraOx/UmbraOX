# C:\Umbra\core\gui\control_center.py
# C:\Umbra\core\ui\umbra_control_center.py  — copy to BOTH
# Umbra Control Center v3.1 — uses tk.Tk() composition, not inheritance
# launch_in_thread() creates window, interactive_mode calls .mainloop() on main thread

import os,sys,json,time,queue,threading,subprocess
import tkinter as tk
from tkinter import ttk,scrolledtext,filedialog,messagebox

_ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BG="#0d0d1a";PANEL="#13132a";BORDER="#2a2a5a";ACCENT="#6a40d4";ACCENT2="#4060c0"
GREEN="#30c060";RED="#c03040";YELLOW="#c0a020";TEXT="#d0d0e8";DIM="#707090"
INP="#1a1a30";BTN="#2a2a50";LOG_BG="#0a0a18";LOG_FG="#a0c0a0"
FM=("Consolas",11);FL=("Segoe UI",10);FT=("Segoe UI",13,"bold");FS=("Consolas",9)

class UmbraControlCenter:
    def __init__(self,runtime=None,process_fn=None):
        self.runtime=runtime;self.process_fn=process_fn
        self._q=queue.Queue();self._history=[];self._hist_idx=0
        self._ws=os.path.join(_ROOT,"workspaces");self._jobs=[];self._job_id=0
        self._running=True;self._prev_photo=None
        self.root=tk.Tk()
        self.root.title("UMBRA — Autonomous AI Runtime OS v2.4.0")
        self.root.configure(bg=BG);self.root.geometry("1400x860");self.root.minsize(1000,600)
        self.root.protocol("WM_DELETE_WINDOW",self._on_close)
        try: self.root.iconbitmap(os.path.join(_ROOT,"core","assets","umbra.ico"))
        except Exception: pass
        self._build_ui();self._start_drain()
        self.log("[UMBRA] Control Center v3.1 ready.",GREEN)

    def mainloop(self): self.root.mainloop()
    def post_message(self,text): self._q.put((str(text),None))
    def log(self,msg,colour=None): self._q.put((str(msg),colour))
    def is_available(self): return True

    def _build_ui(self):
        r=self.root
        tb=tk.Frame(r,bg=PANEL,height=50);tb.pack(fill=tk.X);tb.pack_propagate(False)
        tk.Label(tb,text="⬡  UMBRA",font=FT,fg=ACCENT,bg=PANEL).pack(side=tk.LEFT,padx=16,pady=12)
        tk.Label(tb,text="Autonomous AI Runtime OS",font=FL,fg=DIM,bg=PANEL).pack(side=tk.LEFT)
        self._status_lbl=tk.Label(tb,text="● READY",font=FL,fg=GREEN,bg=PANEL)
        self._status_lbl.pack(side=tk.RIGHT,padx=16)
        self._prog=ttk.Progressbar(r,mode="indeterminate",length=200)
        self._timer_lbl=tk.Label(r,text="",font=FS,fg=YELLOW,bg=PANEL)
        self._task_start=0.0
        pw=tk.PanedWindow(r,orient=tk.HORIZONTAL,bg=BG,sashwidth=5)
        pw.pack(fill=tk.BOTH,expand=True,padx=4,pady=4)
        left=tk.Frame(pw,bg=PANEL,width=200);pw.add(left,minsize=180);self._build_sidebar(left)
        right=tk.Frame(pw,bg=BG);pw.add(right,minsize=700);self._build_tabs(right)

    def _build_sidebar(self,p):
        tk.Label(p,text="QUICK ACTIONS",font=FS,fg=DIM,bg=PANEL).pack(pady=(12,4),padx=8,anchor="w")
        for lbl,cmd in [("📊 Status","status"),("🔧 Fix Bugs","fix all bugs"),
                        ("🎮 Build Game","make a game called MyGame"),
                        ("🖼 Make Image","make an image of a fantasy landscape"),
                        ("🎬 Make GIF","make a gif of fire"),
                        ("📁 List Files","list files"),("🧹 Clean","clean up old files"),
                        ("💾 Projects","projects"),("▶ Play Last","play last"),("📋 Help","help")]:
            tk.Button(p,text=lbl,font=FS,fg=TEXT,bg=BTN,activebackground="#3a3a70",
                      activeforeground=TEXT,relief=tk.FLAT,cursor="hand2",anchor="w",
                      padx=10,command=lambda c=cmd:self._quick(c)).pack(fill=tk.X,padx=6,pady=2)
        tk.Frame(p,bg=BORDER,height=1).pack(fill=tk.X,padx=8,pady=8)
        tk.Button(p,text="✖ Close Umbra",font=FS,fg=TEXT,bg=BTN,activebackground="#3a3a70",
                  activeforeground=TEXT,relief=tk.FLAT,cursor="hand2",anchor="w",
                  padx=10,command=self._on_close).pack(fill=tk.X,padx=6,pady=2)
        tk.Frame(p,bg=BORDER,height=1).pack(fill=tk.X,padx=8,pady=8)
        self._side_info=tk.Label(p,text="Ollama: checking...\nComfyUI: offline",
                                 font=FS,fg=DIM,bg=PANEL,justify=tk.LEFT,wraplength=180)
        self._side_info.pack(padx=8,anchor="w")
        self.root.after(3000,self._update_side_info)

    def _build_tabs(self,p):
        style=ttk.Style();style.theme_use("default")
        style.configure("TNotebook",background=BG,borderwidth=0)
        style.configure("TNotebook.Tab",background=BTN,foreground=DIM,font=FL,padding=[10,5])
        style.map("TNotebook.Tab",background=[("selected",ACCENT)],foreground=[("selected","#ffffff")])
        self._nb=ttk.Notebook(p);self._nb.pack(fill=tk.BOTH,expand=True)
        for label,attr in [("  💬 Console  ","_tc"),("  📋 Task Queue  ","_tq"),
                           ("  📁 Files  ","_tf"),("  🖼 Preview  ","_tp"),
                           ("  🤖 Agents  ","_ta"),("  🧠 Memory  ","_tm")]:
            f=tk.Frame(self._nb,bg=BG);setattr(self,attr,f);self._nb.add(f,text=label)
        self._build_console(self._tc);self._build_taskqueue(self._tq)
        self._build_files(self._tf);self._build_preview(self._tp)
        self._build_agents(self._ta);self._build_memory(self._tm)

    def _build_console(self,p):
        self._out=scrolledtext.ScrolledText(p,bg=LOG_BG,fg=LOG_FG,font=FM,wrap=tk.WORD,
                                            state=tk.DISABLED,relief=tk.FLAT,bd=0)
        self._out.pack(fill=tk.BOTH,expand=True,padx=6,pady=6)
        for tag,col in [("green",GREEN),("red",RED),("yellow",YELLOW),
                        ("accent",ACCENT),("dim",DIM),("white",TEXT)]:
            self._out.tag_config(tag,foreground=col)
        inp=tk.Frame(p,bg=PANEL,pady=6);inp.pack(fill=tk.X,padx=6,pady=(0,6))
        tk.Label(inp,text="umbra >",font=FM,fg=ACCENT,bg=PANEL).pack(side=tk.LEFT,padx=(8,4))
        self._entry=tk.Entry(inp,bg=INP,fg=TEXT,font=FM,relief=tk.FLAT,insertbackground=TEXT,
                             highlightthickness=1,highlightbackground=BORDER,highlightcolor=ACCENT)
        self._entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=4)
        self._entry.bind("<Return>",self._on_enter)
        self._entry.bind("<Up>",self._hist_up);self._entry.bind("<Down>",self._hist_dn)
        self._entry.focus_set()
        tk.Button(inp,text="Send ▶",font=FL,fg="#fff",bg=ACCENT,activebackground=ACCENT2,
                  relief=tk.FLAT,padx=12,cursor="hand2",
                  command=self._on_enter).pack(side=tk.RIGHT,padx=(4,8))

    def _build_taskqueue(self,p):
        tk.Label(p,text="Task Queue — Priority Controls",font=FL,fg=DIM,bg=BG).pack(pady=8,padx=10,anchor="w")
        bar=tk.Frame(p,bg=BG);bar.pack(fill=tk.X,padx=10,pady=(0,4))
        for lbl,cmd,col in [("🔄 Refresh",self._refresh_jobs,TEXT),("⬆ Priority Up",self._job_up,TEXT),
                             ("⬇ Priority Down",self._job_dn,TEXT),("🗑 Remove",self._job_remove,RED)]:
            tk.Button(bar,text=lbl,font=FS,fg=col,bg=BTN,relief=tk.FLAT,padx=8,command=cmd).pack(side=tk.LEFT,padx=2)
        cols=("ID","Task","Type","Status","Priority")
        self._jt=ttk.Treeview(p,columns=cols,show="headings",height=22)
        for c,w in [("ID",50),("Task",380),("Type",100),("Status",100),("Priority",80)]:
            self._jt.heading(c,text=c);self._jt.column(c,width=w)
        sb=ttk.Scrollbar(p,orient=tk.VERTICAL,command=self._jt.yview)
        self._jt.configure(yscrollcommand=sb.set)
        self._jt.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(10,0),pady=4)
        sb.pack(side=tk.LEFT,fill=tk.Y,pady=4)

    def _refresh_jobs(self):
        for i in self._jt.get_children(): self._jt.delete(i)
        for j in self._jobs:
            self._jt.insert("","end",values=(j["id"],j["task"][:60],j["type"],j["status"],j["priority"]))

    def _job_up(self):
        sel=self._jt.selection()
        if not sel: return
        jid=self._jt.item(sel[0])["values"][0]
        for j in self._jobs:
            if j["id"]==jid: j["priority"]=min(10,j["priority"]+1)
        self._jobs.sort(key=lambda x:-x["priority"]);self._refresh_jobs()

    def _job_dn(self):
        sel=self._jt.selection()
        if not sel: return
        jid=self._jt.item(sel[0])["values"][0]
        for j in self._jobs:
            if j["id"]==jid: j["priority"]=max(1,j["priority"]-1)
        self._jobs.sort(key=lambda x:-x["priority"]);self._refresh_jobs()

    def _job_remove(self):
        sel=self._jt.selection()
        if not sel: return
        jid=self._jt.item(sel[0])["values"][0]
        self._jobs=[j for j in self._jobs if j["id"]!=jid];self._refresh_jobs()

    def add_job(self,task,task_type="general",status="queued",priority=5):
        self._job_id+=1
        self._jobs.append({"id":self._job_id,"task":task,"type":task_type,
                           "status":status,"priority":priority})
        self._jobs.sort(key=lambda x:-x["priority"])
        self.root.after(0,self._refresh_jobs)

    def update_job_status(self,task,status):
        for j in self._jobs:
            if task in j["task"]: j["status"]=status
        self.root.after(0,self._refresh_jobs)

    def _build_files(self,p):
        tk.Label(p,text="Workspace Files",font=FL,fg=DIM,bg=BG).pack(pady=8,padx=10,anchor="w")
        bar=tk.Frame(p,bg=BG);bar.pack(fill=tk.X,padx=10,pady=(0,4))
        for lbl,cmd,col in [("🔄 Refresh",self._refresh_files,TEXT),("📂 Open",self._open_ws,TEXT),
                             ("▶ Run",self._run_sel,TEXT),("🖼 Preview",self._preview_sel,TEXT),
                             ("🗑 Delete",self._del_sel,RED)]:
            tk.Button(bar,text=lbl,font=FS,fg=col,bg=BTN,relief=tk.FLAT,padx=8,command=cmd).pack(side=tk.LEFT,padx=2)
        cols=("Name","Size","Modified","Type")
        self._ft=ttk.Treeview(p,columns=cols,show="headings",height=22)
        for c,w in [("Name",320),("Size",80),("Modified",140),("Type",80)]:
            self._ft.heading(c,text=c);self._ft.column(c,width=w)
        sb2=ttk.Scrollbar(p,orient=tk.VERTICAL,command=self._ft.yview)
        self._ft.configure(yscrollcommand=sb2.set)
        self._ft.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(10,0),pady=4)
        sb2.pack(side=tk.LEFT,fill=tk.Y,pady=4)
        self._ft.bind("<Double-1>",lambda e:self._run_sel())
        self._refresh_files()

    def _refresh_files(self):
        for i in self._ft.get_children(): self._ft.delete(i)
        if not os.path.isdir(self._ws): return
        for root,dirs,files in os.walk(self._ws):
            dirs[:]=[d for d in dirs if d not in ("__pycache__",".git")]
            level=root.replace(self._ws,"").count(os.sep)
            if level>3: continue
            rel=os.path.relpath(root,self._ws)
            if rel!=".": self._ft.insert("","end",values=("📁 "+rel+"/","","","folder"),tags=("",))
            for fn in sorted(files)[:30]:
                fp=os.path.join(root,fn)
                try:
                    sz=os.path.getsize(fp)
                    mod=time.strftime("%Y-%m-%d %H:%M",time.localtime(os.path.getmtime(fp)))
                    ext=os.path.splitext(fn)[1]
                    self._ft.insert("","end",values=(fn,f"{sz//1024}KB" if sz>1024 else f"{sz}B",mod,ext),tags=(fp,))
                except Exception: pass

    def _open_ws(self):
        os.makedirs(self._ws,exist_ok=True)
        if sys.platform=="win32": os.startfile(self._ws)
        else: subprocess.Popen(["xdg-open",self._ws])

    def _sel_path(self):
        sel=self._ft.selection()
        if not sel: return None
        tags=self._ft.item(sel[0],"tags")
        return tags[0] if tags and tags[0] and os.path.isfile(tags[0]) else None

    def _run_sel(self):
        fp=self._sel_path()
        if fp and fp.endswith(".py"):
            subprocess.Popen([sys.executable,fp],cwd=os.path.dirname(fp))
            self.log("[GUI] Launched: "+fp,GREEN)

    def _preview_sel(self):
        fp=self._sel_path()
        if not fp: return
        if os.path.splitext(fp)[1].lower() in (".png",".jpg",".jpeg",".gif",".bmp"):
            self._show_preview(fp);self._nb.select(self._tp)

    def _del_sel(self):
        fp=self._sel_path()
        if not fp: return
        if messagebox.askyesno("Delete",f"Delete {os.path.basename(fp)}?"):
            try: os.remove(fp);self.log("[GUI] Deleted: "+fp,YELLOW);self._refresh_files()
            except Exception as e: self.log("[GUI] Error: "+str(e),RED)

    def _build_preview(self,p):
        tk.Label(p,text="Image / Video Preview",font=FL,fg=DIM,bg=BG).pack(pady=8,padx=10,anchor="w")
        bar=tk.Frame(p,bg=BG);bar.pack(fill=tk.X,padx=10,pady=(0,4))
        tk.Button(bar,text="📂 Browse",font=FS,fg=TEXT,bg=BTN,relief=tk.FLAT,
                  padx=8,command=self._browse_img).pack(side=tk.LEFT,padx=2)
        tk.Button(bar,text="🔄 Latest",font=FS,fg=TEXT,bg=BTN,relief=tk.FLAT,
                  padx=8,command=self._load_latest).pack(side=tk.LEFT,padx=2)
        self._prev_lbl=tk.Label(p,bg=BG,fg=DIM,font=FL,wraplength=700,
                                text="No image loaded.\nGenerate one with: make an image of a dragon")
        self._prev_lbl.pack(fill=tk.BOTH,expand=True,padx=20,pady=20)
        self._prev_info=tk.Label(p,text="",fg=DIM,bg=BG,font=FS)
        self._prev_info.pack(pady=4)

    def _show_preview(self,path):
        try:
            from PIL import Image,ImageTk
            img=Image.open(path);img.thumbnail((750,520),Image.LANCZOS)
            self._prev_photo=ImageTk.PhotoImage(img)
            self._prev_lbl.configure(image=self._prev_photo,text="")
            sz=os.path.getsize(path)
            self._prev_info.configure(text=f"{os.path.basename(path)}  |  {img.size[0]}x{img.size[1]}  |  {sz//1024}KB")
        except ImportError:
            self._prev_lbl.configure(text=f"Install Pillow: pip install Pillow\nFile: {path}",image="")
        except Exception as e:
            self._prev_lbl.configure(text=f"Cannot preview: {e}",image="")

    def _browse_img(self):
        fp=filedialog.askopenfilename(title="Open Image",
                                      initialdir=os.path.join(self._ws,"images"),
                                      filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.bmp"),("All","*.*")])
        if fp: self._show_preview(fp)

    def _load_latest(self):
        img_dir=os.path.join(self._ws,"images")
        if not os.path.isdir(img_dir): return
        imgs=[(os.path.getmtime(os.path.join(img_dir,f)),os.path.join(img_dir,f))
              for f in os.listdir(img_dir) if f.lower().endswith((".png",".jpg",".jpeg",".gif"))]
        if imgs:
            imgs.sort(reverse=True);self._show_preview(imgs[0][1]);self._nb.select(self._tp)

    def _build_agents(self,p):
        tk.Label(p,text="Agent Status",font=FL,fg=DIM,bg=BG).pack(pady=8,padx=10,anchor="w")
        agents=[("World Agent","World map, biomes, towns, bandit camps"),
                ("Character Agent","Player, Enemy, NPC classes and stats"),
                ("Item Agent","Weapons, armor, spells, loot tables"),
                ("Mechanic Agent","Combat, crafting, save/load systems"),
                ("UI Agent","HUD, menus, inventory, dialogue panels"),
                ("Quest Agent","Quest data, spawn logic, progression"),
                ("Economy Agent","Shops, crafting recipes, building costs"),
                ("Image Agent","ComfyUI image generation pipeline"),
                ("Sprite Agent","PIL pixel-art sprite generator"),
                ("GIF Agent","PIL animated GIF generator"),
                ("TTS Agent","Text-to-speech via pyttsx3"),
                ("Voice Agent","Speech recognition input"),
                ("Code Agent","Ollama code generation pipeline"),
                ("Repair Agent","Syntax checking and auto-repair")]
        cols=("Agent","Description","Status")
        self._ag=ttk.Treeview(p,columns=cols,show="headings",height=18)
        self._ag.heading("Agent",text="Agent");self._ag.column("Agent",width=160)
        self._ag.heading("Description",text="Description");self._ag.column("Description",width=400)
        self._ag.heading("Status",text="Status");self._ag.column("Status",width=100)
        for name,desc in agents: self._ag.insert("","end",values=(name,desc,"standby"))
        sb3=ttk.Scrollbar(p,orient=tk.VERTICAL,command=self._ag.yview)
        self._ag.configure(yscrollcommand=sb3.set)
        self._ag.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=4)
        sb3.pack(side=tk.LEFT,fill=tk.Y,pady=4)

    def update_agent_status(self,agent_name,status):
        for item in self._ag.get_children():
            vals=self._ag.item(item)["values"]
            if vals and agent_name.lower() in str(vals[0]).lower():
                self._ag.item(item,values=(vals[0],vals[1],status));break

    def _build_memory(self,p):
        tk.Label(p,text="Runtime Memory",font=FL,fg=DIM,bg=BG).pack(pady=8,padx=10,anchor="w")
        bar=tk.Frame(p,bg=BG);bar.pack(fill=tk.X,padx=10,pady=(0,4))
        tk.Button(bar,text="🔄 Refresh",font=FS,fg=TEXT,bg=BTN,relief=tk.FLAT,
                  padx=8,command=self._refresh_mem).pack(side=tk.LEFT,padx=2)
        tk.Label(bar,text="Search:",fg=DIM,bg=BG,font=FS).pack(side=tk.LEFT,padx=(10,4))
        self._mem_srch=tk.Entry(bar,bg=INP,fg=TEXT,font=FS,width=30,relief=tk.FLAT)
        self._mem_srch.pack(side=tk.LEFT)
        self._mem_srch.bind("<Return>",lambda e:self._refresh_mem())
        cols=("Key","Value","Tags")
        self._mt=ttk.Treeview(p,columns=cols,show="headings",height=22)
        for c,w in [("Key",200),("Value",400),("Tags",160)]:
            self._mt.heading(c,text=c);self._mt.column(c,width=w)
        sb4=ttk.Scrollbar(p,orient=tk.VERTICAL,command=self._mt.yview)
        self._mt.configure(yscrollcommand=sb4.set)
        self._mt.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(10,0),pady=4)
        sb4.pack(side=tk.LEFT,fill=tk.Y,pady=4)

    def _refresh_mem(self):
        for i in self._mt.get_children(): self._mt.delete(i)
        if not self.runtime: return
        mem=(self.runtime.get("memory") if isinstance(self.runtime,dict)
             else getattr(self.runtime,"memory",None))
        if not mem: return
        q=self._mem_srch.get().strip().lower()
        try:
            for e in (mem.list_all() if hasattr(mem,"list_all") else []):
                k=str(e.get("key",""));v=str(e.get("value",""))[:120];t=str(e.get("tags",""))
                if not q or q in k.lower() or q in v.lower():
                    self._mt.insert("","end",values=(k,v,t))
        except Exception: pass

    def _update_timer(self):
        if not self._running: return
        try:
            elapsed=time.time()-self._task_start
            self._timer_lbl.configure(text=f"  ⏱ Elapsed: {elapsed:.0f}s")
            if self._prog.winfo_ismapped():
                self.root.after(1000,self._update_timer)
        except Exception: pass

    def _start_drain(self): self.root.after(50,self._drain)

    def _drain(self):
        if not self._running: return
        try:
            count=0
            while count<50:
                msg,col=self._q.get_nowait();self._write(msg,col);count+=1
        except queue.Empty: pass
        self.root.after(50,self._drain)

    def _write(self,msg,col=None):
        self._out.configure(state=tk.NORMAL)
        ts=time.strftime("%H:%M:%S");low=msg.lower()
        if col:
            rev={GREEN:"green",RED:"red",YELLOW:"yellow",ACCENT:"accent",DIM:"dim"}
            tag=rev.get(col,"white")
        elif any(x in low for x in ["[error]","[fail]","failed","error:"]):tag="red"
        elif any(x in low for x in ["[ok]","[done]","complete","saved","built","ready","✓"]):tag="green"
        elif any(x in low for x in ["[warn]","warning","missing","offline","stream error"]):tag="yellow"
        elif any(x in low for x in ["[umbra]","[agent","[plan]","[build]","[stitch]","[you]","[syntax]","[test]"]):tag="accent"
        elif msg.startswith("  ") or msg.startswith("[") or msg.startswith("╔") or msg.startswith("╚"):tag="dim"
        else:tag="white"
        self._out.insert(tk.END,f"[{ts}] {msg}\n",tag)
        self._out.see(tk.END);self._out.configure(state=tk.DISABLED)

    def _on_enter(self,event=None):
        text=self._entry.get().strip()
        if not text: return
        self._entry.delete(0,tk.END)
        if not self._history or self._history[-1]!=text: self._history.append(text)
        self._hist_idx=len(self._history)
        self.log(f"[YOU] {text}",ACCENT);self._send(text)

    def _send(self,text):
        ttype=("game" if any(w in text.lower() for w in ["game","rpg"])
               else "image" if "image" in text.lower()
               else "gif" if "gif" in text.lower() else "general")
        self.add_job(text,ttype,"running")
        self._task_start=time.time()
        self._prog.pack(fill=tk.X);self._prog.start(10)
        self._timer_lbl.pack(fill=tk.X)
        self._status_lbl.configure(text="● WORKING",fg=YELLOW)
        self._update_timer()
        def _run():
            try:
                if self.process_fn and self.runtime: self.process_fn(self.runtime,text)
                elif self.runtime:
                    for attr in ("run_prompt","process","handle"):
                        fn=getattr(self.runtime,attr,None)
                        if fn: fn(text);break
                else: self.log("[GUI] No runtime.",YELLOW)
            except Exception as e:
                self.log(f"[ERROR] {e}",RED)
            finally:
                self.root.after(0,self._task_done)
                self.update_job_status(text,"done")
        threading.Thread(target=_run,daemon=True).start()

    def _task_done(self):
        try: self._prog.stop();self._prog.pack_forget()
        except Exception: pass
        try: self._timer_lbl.pack_forget()
        except Exception: pass
        elapsed=time.time()-self._task_start
        self._status_lbl.configure(text=f"● READY  (last task: {elapsed:.0f}s)",fg=GREEN)
        self._refresh_files()
        self.root.after(500,self._load_latest)

    def _quick(self,cmd):
        self._entry.delete(0,tk.END);self._entry.insert(0,cmd);self._on_enter()

    def _hist_up(self,e=None):
        if not self._history: return
        self._hist_idx=max(0,self._hist_idx-1)
        self._entry.delete(0,tk.END);self._entry.insert(0,self._history[self._hist_idx])

    def _hist_dn(self,e=None):
        if not self._history: return
        self._hist_idx=min(len(self._history),self._hist_idx+1)
        self._entry.delete(0,tk.END)
        if self._hist_idx<len(self._history): self._entry.insert(0,self._history[self._hist_idx])

    def _update_side_info(self):
        def _chk(url):
            try:
                import urllib.request;urllib.request.urlopen(url,timeout=1).close();return True
            except Exception: return False
        o="online ✓" if _chk("http://localhost:11434/api/tags") else "offline"
        c="online ✓" if _chk("http://127.0.0.1:8188/system_stats") else "offline"
        self._side_info.configure(text=f"Ollama: {o}\nComfyUI: {c}")
        self.root.after(15000,self._update_side_info)

    def _on_close(self):
        if messagebox.askyesno("Close Umbra","Close Umbra completely?"):
            self._running=False
            try: self.root.destroy()
            except Exception: pass
            import os as _os;_os._exit(0)


def launch_in_thread(runtime=None,process_fn=None):
    """Create GUI window. Caller must call .mainloop() on main thread."""
    return UmbraControlCenter(runtime=runtime,process_fn=process_fn)

def launch_control_center(runtime=None,process_fn=None):
    app=UmbraControlCenter(runtime=runtime,process_fn=process_fn)
    app.mainloop();return app

if __name__=="__main__":
    app=UmbraControlCenter()
    app.log("Standalone test — no runtime",YELLOW)
    app.mainloop()