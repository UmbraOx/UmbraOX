import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_and_read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        s = f.read()
    with open(fp + f".bak56_{ts}", "w", encoding="utf-8") as f:
        f.write(s)
    return s

# ============================================================
# 1. Umbra.py: wire the six GUI-missing commands (same bug class
#    as batch27's "listen" fix - these existed only in
#    interactive_mode's CLI-only elif chain)
# ============================================================
FP1 = r"C:\Umbra\Umbra.py"
src1 = backup_and_read(FP1)

OLD1 = '''        return

    # Self-repair
    if cmd in ("fix", "fix yourself", "fix all bugs", "fix all errors",
               "fix all issues", "repair yourself", "fix everything",'''

NEW1 = '''        return

    # Diagnostics / files / projects (were interactive_mode-CLI-only,
    # same gap batch27 fixed for listen/voice - GUI never reached these)
    if cmd in ("health", "health check", "system health"):
        report = runtime["health"].run_all_checks()
        _umbra_print("\\n[HEALTH] " + report.summary_line())
        for check in report.checks:
            icon = "+" if check["status"] == "pass" else "!"
            _umbra_print("  " + icon + " " + check["name"] + ": " + (check["message"] or check["status"]))
        _umbra_print("")
        return

    if cmd in ("memory", "what do you remember"):
        mem = runtime["memory"]
        stats = mem.get_stats()
        _umbra_print("\\n[MEMORY] " + str(stats["total_entries"]) + " entries")
        for k in mem.list_keys()[:10]:
            _umbra_print("  " + k)
        _umbra_print("")
        return

    if cmd in ("projects", "list projects", "my projects"):
        if pm:
            _projects = pm.list_projects()
            if not _projects:
                _umbra_print("  No projects yet.\\n")
            else:
                _umbra_print("\\n[PROJECTS] " + str(len(_projects)) + " total:")
                for p in _projects:
                    tag = " (active)" if (active and active.slug == p.slug) else ""
                    _umbra_print("  " + p.name + tag + " | " + str(len(p.files)) + " files")
                _umbra_print("")
        return

    if (cmd.startswith("work on ") or cmd.startswith("lets work on ")
            or cmd.startswith("continue ") or cmd.startswith("open ")):
        _wname = None
        for pfx in ("lets work on ", "work on ", "continue ", "open "):
            if cmd.startswith(pfx):
                _wname = user_input[len(pfx):].strip().title()
                break
        if _wname and pm:
            _existing = pm.get_project(_wname)
            if _existing:
                pm.set_active(_wname)
                _umbra_print("\\n[UMBRA] Switched to: " + _existing.name + "\\n")
            else:
                _umbra_print("  Project '" + _wname + "' not found.\\n")
        return

    if cmd in ("list files", "show files", "browse files", "files"):
        handle_files_browser(runtime, cmd)
        return

    if "list workspace" in cmd or "workspace files" in cmd:
        handle_files_browser(runtime, "workspace")
        return

    if "clean" in cmd and ("file" in cmd or "old" in cmd or "backup" in cmd):
        handle_files_browser(runtime, "clean old files")
        return

    # Self-repair
    if cmd in ("fix", "fix yourself", "fix all bugs", "fix all errors",
               "fix all issues", "repair yourself", "fix everything",'''

if OLD1 not in src1:
    print("FAIL: GUI-command anchor not found")
    sys.exit(1)
if src1.count(OLD1) != 1:
    print("FAIL: GUI-command anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD1, NEW1, 1)

# ============================================================
# 2. Umbra.py: fix TTS - remove silent failure, reuse engine
#    instance (avoids repeated COM-object churn that's the most
#    common cause of pyttsx3 silently doing nothing when called
#    from a background thread, which is how the GUI calls it)
# ============================================================
OLD2 = '''def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            tts_mod.run(text)
            return
        if not _ensure_pyttsx3():
            return
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass'''

NEW2 = '''def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            tts_mod.run(text)
            return
        if not _ensure_pyttsx3():
            return
        # pyttsx3's SAPI5 driver on Windows is backed by a COM object that
        # is NOT safe to re-create on every call from a background thread
        # (which is how the GUI invokes this) - that mismatch is the most
        # common reason "tts on" silently does nothing at all. Initialize
        # COM for this thread if pywin32 is available, and reuse a single
        # cached engine instance instead of creating a new one every call.
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except Exception:
            pass
        engine = runtime.get("_tts_pyttsx3_engine")
        if engine is None:
            import pyttsx3
            engine = pyttsx3.init()
            runtime["_tts_pyttsx3_engine"] = engine
        engine.say(text)
        engine.runAndWait()
    except Exception as _tts_ex:
        # Was a bare "except: pass" - meant "tts on" could fail completely
        # silently with zero feedback, which is exactly what was reported.
        _umbra_print("  [TTS] Error: " + str(_tts_ex) + "\\n")'''

if OLD2 not in src1:
    print("FAIL: TTS anchor not found")
    sys.exit(1)
if src1.count(OLD2) != 1:
    print("FAIL: TTS anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD2, NEW2, 1)

with open(FP1, "w", encoding="utf-8") as f:
    f.write(src1)

try:
    ast.parse(src1)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL (Umbra.py): " + str(e))
    sys.exit(1)

# ============================================================
# 3. runtime_memory_store.py: recall by keyword overlap, not
#    exact substring containment
# ============================================================
FP2 = r"C:\Umbra\core\runtime\runtime_memory_store.py"
src2 = backup_and_read(FP2)

OLD3 = '''    def search(self, query, top_k=10):
        query_lower = query.lower()
        results = []
        for entry in self.entries.values():
            score = 0
            if query_lower in str(entry.value).lower():
                score += 2
            if query_lower in entry.key.lower():
                score += 3
            if any(query_lower in tag.lower() for tag in entry.tags):
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in results[:top_k]]'''

NEW3 = '''    def search(self, query, top_k=10):
        # Was pure substring containment ("games I like" not found in
        # "I like the games..." because word order differs) - use keyword
        # overlap instead so word order in the query doesn't matter, while
        # still rewarding an exact-phrase hit as a bonus.
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 1]
        results = []
        for entry in self.entries.values():
            value_lower = str(entry.value).lower()
            key_lower = entry.key.lower()
            tags_lower = [t.lower() for t in entry.tags]
            score = 0
            if query_lower in value_lower:
                score += 2
            if query_lower in key_lower:
                score += 3
            if any(query_lower in t for t in tags_lower):
                score += 1
            if query_words:
                value_hits = sum(1 for w in query_words if w in value_lower)
                key_hits = sum(1 for w in query_words if w in key_lower)
                score += value_hits
                score += key_hits * 2
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in results[:top_k]]'''

if OLD3 not in src2:
    print("FAIL: search() anchor not found")
    sys.exit(1)
if src2.count(OLD3) != 1:
    print("FAIL: search() anchor not unique")
    sys.exit(1)
src2 = src2.replace(OLD3, NEW3, 1)

with open(FP2, "w", encoding="utf-8") as f:
    f.write(src2)

try:
    ast.parse(src2)
    print("runtime_memory_store.py AST OK")
except SyntaxError as e:
    print("AST FAIL (memory store): " + str(e))
    sys.exit(1)

print("Fix applied: 6 GUI-missing commands wired, TTS silent-failure+threading fixed, recall uses keyword matching (batch56)")