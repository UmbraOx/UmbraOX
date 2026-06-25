"""
umbra_dev_assistant.py  v2.0  —  Umbra Dev Assistant
=====================================================
Local Claude-like capabilities inside Umbra:
  show <file> [lines X-Y]     — read any file with line numbers
  edit <file>: <instruction>  — LLM edits file, shows diff, asks approval, backs up
  search for <term>           — grep across all Umbra .py files
  list files                  — show key file map
  run tests                   — run test_umbra_full.py and show results
  clear history               — reset conversation memory
  which model                 — show active chat model
  <anything else>             — multi-turn dev chat with code output

Wire into Umbra.py _process_command() — see bottom of file.
"""

import os, re, difflib, shutil, datetime, subprocess, sys

_chat_history = []
_MAX_HISTORY  = 20
_UMBRA_ROOT   = os.path.dirname(os.path.abspath(__file__))

_PATH_ALIASES = {
    "umbra.py":              os.path.join(_UMBRA_ROOT, "Umbra.py"),
    "umbra":                 os.path.join(_UMBRA_ROOT, "Umbra.py"),
    "control_center.py":     os.path.join(_UMBRA_ROOT, "core", "gui", "control_center.py"),
    "control_center":        os.path.join(_UMBRA_ROOT, "core", "gui", "control_center.py"),
    "game_skeleton.py":      os.path.join(_UMBRA_ROOT, "core", "assets", "game_skeleton.py"),
    "game_skeleton":         os.path.join(_UMBRA_ROOT, "core", "assets", "game_skeleton.py"),
    "runtime_spine.py":      os.path.join(_UMBRA_ROOT, "core", "runtime", "umbra_runtime_spine.py"),
    "task_engine.py":        os.path.join(_UMBRA_ROOT, "core", "runtime", "umbra_task_engine.py"),
    "generation_engine.py":  os.path.join(_UMBRA_ROOT, "core", "runtime", "umbra_generation_engine.py"),
    "runtime_kernel.py":     os.path.join(_UMBRA_ROOT, "core", "runtime", "umbra_runtime_kernel.py"),
    "gif_generator.py":      os.path.join(_UMBRA_ROOT, "core", "runtime", "runtime_animated_gif_generator.py"),
    "image_generator.py":    os.path.join(_UMBRA_ROOT, "core", "runtime", "runtime_image_generator.py"),
    "dev_assistant.py":      os.path.join(_UMBRA_ROOT, "umbra_dev_assistant.py"),
    "test_umbra_full.py":    os.path.join(_UMBRA_ROOT, "test_umbra_full.py"),
    "tests":                 os.path.join(_UMBRA_ROOT, "test_umbra_full.py"),
}


# ── Path resolver ─────────────────────────────────────────────────────────────

def _resolve_path(name):
    name = name.strip().strip("'\"")
    key  = name.lower()
    if key in _PATH_ALIASES:
        return _PATH_ALIASES[key]
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for base in [_UMBRA_ROOT,
                 os.path.join(_UMBRA_ROOT, "core", "runtime"),
                 os.path.join(_UMBRA_ROOT, "core", "gui"),
                 os.path.join(_UMBRA_ROOT, "core", "assets")]:
        c = os.path.join(base, name)
        if os.path.exists(c):
            return c
    for root, dirs, files in os.walk(_UMBRA_ROOT):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "venv")]
        if os.path.basename(name) in files:
            return os.path.join(root, os.path.basename(name))
    return None


# ── Model picker ──────────────────────────────────────────────────────────────

def _pick_chat_model():
    import urllib.request as _ur, json as _j
    try:
        with _ur.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            models = [m["name"] for m in _j.loads(r.read()).get("models", [])]
    except Exception:
        models = []
    # qwen3:14b is the best general model already installed
    preference = [
        "qwen3:14b", "qwen3:latest",
        "llama3.1:70b", "qwen2.5:72b",
        "llama3.1:8b", "qwen2.5:7b", "llama3:latest",
        "mistral:7b", "qwen2.5-coder:32b", "qwen2.5-coder:14b",
        "deepseek-r1:latest", "qwen2.5-coder:7b",
    ]
    for p in preference:
        if p in models:
            return p
    return models[0] if models else "qwen2.5-coder:32b"


# ── Ollama chat (messages API, keeps conversation context) ────────────────────

def _ollama_chat(prompt, system=None, timeout=300):
    import urllib.request as _ur, json as _j
    model    = _pick_chat_model()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    for t in _chat_history[-_MAX_HISTORY:]:
        messages.append({"role": t["role"], "content": t["content"]})
    messages.append({"role": "user", "content": prompt})

    payload = _j.dumps({
        "model": model, "messages": messages, "stream": True,
        "options": {"num_predict": -1, "temperature": 0.2, "top_p": 0.9}
    }).encode("utf-8")
    req = _ur.Request("http://localhost:11434/api/chat", data=payload,
                      headers={"Content-Type": "application/json"}, method="POST")
    parts = []
    try:
        with _ur.urlopen(req, timeout=timeout) as resp:
            while True:
                line = resp.readline()
                if not line: break
                try:
                    chunk = _j.loads(line.decode("utf-8", errors="replace"))
                    parts.append(chunk.get("message", {}).get("content", ""))
                    if chunk.get("done"): break
                except Exception:
                    continue
    except Exception as ex:
        return f"[STREAM ERROR] {ex}"
    return "".join(parts)


# ── Intent detection ──────────────────────────────────────────────────────────

_SHOW_RE    = re.compile(
    r"^(?:show|read|open|view|display|print)\s+(?:me\s+)?(?:file\s+)?(.+?)"
    r"(?:\s+(?:lines?\s*)?(\d+)\s*[-–to]+\s*(\d+))?$", re.IGNORECASE)
_EDIT_RE    = re.compile(
    r"^(?:edit|update|patch|change|modify|rewrite)\s+(?:file\s+)?(.+?)(?:\s*[:\-–]\s*(.+))?$",
    re.IGNORECASE)
_SEARCH_RE  = re.compile(
    r"^(?:search|grep|find|look for)\s+(?:for\s+)?(?:all\s+)?(?:uses?\s+of\s+)?(.+?)(?:\s+in\s+(.+))?$",
    re.IGNORECASE)
_LIST_RE    = re.compile(r"^(?:list|ls)\s*(?:files?|all files?)?$", re.IGNORECASE)
_TEST_RE    = re.compile(r"^(?:run\s+)?tests?$", re.IGNORECASE)
_CLEAR_RE   = re.compile(r"^(?:clear|reset)\s+(?:chat|history|memory|context)$", re.IGNORECASE)
_MODEL_RE   = re.compile(r"^(?:which|what)\s+model\??$", re.IGNORECASE)

_CHAT_TRIGGERS = (
    "explain","how does","how do","why does","what is","what are","tell me",
    "describe","summarize","help me","can you","could you","add a","implement",
    "write code","write a","create a function","what would","is there","does umbra",
    "what's","whats","how would","give me","show me how",
)


def detect_intent(user_input):
    cmd = user_input.strip()
    if _CLEAR_RE.match(cmd):   return "clear_history", {}
    if _MODEL_RE.match(cmd):   return "which_model", {}
    if _LIST_RE.match(cmd):    return "list_files", {}
    if _TEST_RE.match(cmd):    return "run_tests", {}

    m = _SEARCH_RE.match(cmd)
    if m: return "search_code", {"term": m.group(1).strip(), "scope": m.group(2)}

    m = _SHOW_RE.match(cmd)
    if m:
        fname = m.group(1).strip()
        if ("." in fname or fname.lower() in _PATH_ALIASES or
                any(fname.lower().startswith(k) for k in _PATH_ALIASES)):
            return "show_file", {
                "name":  fname,
                "start": int(m.group(2)) if m.group(2) else None,
                "end":   int(m.group(3)) if m.group(3) else None,
            }

    m = _EDIT_RE.match(cmd)
    if m:
        fname = m.group(1).strip()
        if "." in fname or fname.lower() in _PATH_ALIASES:
            return "edit_file", {"name": fname, "instruction": (m.group(2) or "").strip()}

    low = cmd.lower()
    if any(low.startswith(t) for t in _CHAT_TRIGGERS) or cmd.endswith("?"):
        return "chat", {"message": cmd}

    return None, None


# ── Handlers ──────────────────────────────────────────────────────────────────

def handle_show_file(name, start=None, end=None, print_fn=print):
    path = _resolve_path(name)
    if not path:
        print_fn(f"[DEV] File not found: {name}")
        return
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
        total = len(all_lines)
        s = max(0, (start or 1) - 1)
        e = min(total, end or total)
        lines = [(i + 1, all_lines[i].rstrip("\n")) for i in range(s, e)]
        rel = os.path.relpath(path, _UMBRA_ROOT)
        print_fn(f"\n[FILE] {rel}  ({total} lines total)\n")
        header = f"┌─ {rel} (lines {lines[0][0]}-{lines[-1][0]})"
        print_fn(header)
        for no, text in lines:
            print_fn(f"│  {no:5d}  {text}")
        print_fn("└" + "─" * (len(header) - 1))
        print_fn("")
        _chat_history.append({"role": "assistant",
                               "content": f"[Showed {rel} lines {lines[0][0]}-{lines[-1][0]}]"})
    except Exception as e:
        print_fn(f"[DEV] Read error: {e}")


def handle_search_code(term, scope=None, print_fn=print):
    search_root = _UMBRA_ROOT
    if scope:
        p = _resolve_path(scope)
        if p and os.path.isfile(p):
            _search_file(p, term, print_fn)
            return
        if p and os.path.isdir(p):
            search_root = p
    print_fn(f"\n[SEARCH] '{term}'\n")
    total = 0
    for root, dirs, files in os.walk(search_root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "venv")]
        for fname in sorted(files):
            if not fname.endswith(".py"): continue
            hits = _search_file(os.path.join(root, fname), term, print_fn, quiet=True)
            total += hits
            if total > 300:
                print_fn("  ... (truncated)")
                return
    print_fn(f"\n  {total} match(es) found.\n")


def _search_file(path, term, print_fn, quiet=False):
    rel  = os.path.relpath(path, _UMBRA_ROOT)
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                if term.lower() in line.lower():
                    hits.append((i, line.rstrip()))
    except Exception:
        return 0
    if hits:
        print_fn(f"\n  ── {rel}")
        for lineno, text in hits[:20]:
            print_fn(f"     {lineno:5d}  {text.replace(term, f'»{term}«')}")
        if len(hits) > 20:
            print_fn(f"     ... ({len(hits)-20} more)")
    return len(hits)


def handle_list_files(print_fn=print):
    important = [
        ("Umbra.py",                                    "Main runtime"),
        ("umbra_dev_assistant.py",                      "Dev assistant (this file)"),
        ("test_umbra_full.py",                          "67-test suite"),
        ("core/gui/control_center.py",                  "GUI — 5-tab Control Center"),
        ("core/assets/game_skeleton.py",                "Game template"),
        ("core/runtime/umbra_runtime_spine.py",         "Wiring layer"),
        ("core/runtime/umbra_task_engine.py",           "Task manager"),
        ("core/runtime/umbra_generation_engine.py",     "Generation router"),
        ("core/runtime/umbra_runtime_kernel.py",        "Kernel"),
        ("core/runtime/runtime_animated_gif_generator.py", "GIF generator"),
        ("core/runtime/runtime_image_generator.py",     "Image generator"),
        ("core/runtime/runtime_image_pipeline.py",      "Image pipeline"),
        ("core/runtime/runtime_music_pipeline.py",      "Music pipeline"),
        ("core/runtime/runtime_video_pipeline.py",      "Video pipeline"),
    ]
    print_fn("\n[FILES] Key Umbra files:\n")
    for rel, desc in important:
        full   = os.path.join(_UMBRA_ROOT, rel)
        exists = "✓" if os.path.exists(full) else "✗"
        lc     = ""
        if os.path.exists(full):
            try:
                lc = f"  ({sum(1 for _ in open(full, 'r', encoding='utf-8', errors='replace'))} lines)"
            except Exception: pass
        print_fn(f"  {exists} {rel}{lc}")
        print_fn(f"      {desc}")
    print_fn("")


def handle_run_tests(print_fn=print):
    test_path = os.path.join(_UMBRA_ROOT, "test_umbra_full.py")
    if not os.path.exists(test_path):
        print_fn("[TEST] test_umbra_full.py not found.")
        return
    print_fn("\n[TEST] Running test_umbra_full.py ...\n")
    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True, text=True, timeout=120,
            cwd=_UMBRA_ROOT
        )
        output = (result.stdout + result.stderr).strip()
        # Show last 60 lines
        lines = output.splitlines()
        if len(lines) > 60:
            print_fn(f"  ... (showing last 60 of {len(lines)} lines)")
            lines = lines[-60:]
        for ln in lines:
            print_fn(ln)
        # Summary line
        passed = output.count("PASS")
        failed = output.count("FAIL")
        print_fn(f"\n[TEST] {passed} passed, {failed} failed  (exit code {result.returncode})\n")
        _chat_history.append({"role": "assistant",
                               "content": f"[Tests: {passed} passed, {failed} failed]"})
    except subprocess.TimeoutExpired:
        print_fn("[TEST] Timed out after 120s")
    except Exception as e:
        print_fn(f"[TEST] Error: {e}")


def handle_edit_file(name, instruction, print_fn=print, approval_fn=None):
    path = _resolve_path(name)
    if not path:
        print_fn(f"[DEV] File not found: {name}")
        return
    rel = os.path.relpath(path, _UMBRA_ROOT)
    print_fn(f"\n[EDIT] {rel}")
    print_fn(f"[EDIT] Instruction: {instruction}\n")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()
    except Exception as e:
        print_fn(f"[EDIT] Read error: {e}")
        return

    system = (
        "You are Umbra's self-editing assistant. "
        "Return ONLY the complete modified Python file. "
        "No markdown fences, no explanation, no preamble. Just the file."
    )
    user_prompt = (
        f"File: {rel}\nInstruction: {instruction}\n\n"
        f"Current content:\n{original[:10000]}"
        + (f"\n...(truncated, {len(original)} chars total)" if len(original) > 10000 else "")
    )
    print_fn("[EDIT] Generating edit...")
    modified = _ollama_chat(user_prompt, system=system, timeout=600)
    if not modified or len(modified.strip()) < 50:
        print_fn("[EDIT] LLM returned empty response.")
        return
    modified = re.sub(r"^```(?:python)?\n?", "", modified.strip())
    modified = re.sub(r"\n?```$", "", modified.strip())

    diff_lines = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        modified.splitlines(keepends=True),
        fromfile=f"a/{rel}", tofile=f"b/{rel}", lineterm=""
    ))
    if not diff_lines:
        print_fn("[EDIT] No changes — file already matches.")
        return

    print_fn("\n" + "─" * 60)
    print_fn("[DIFF] Proposed changes:")
    for ln in diff_lines[:80]:
        print_fn(ln)
    if len(diff_lines) > 80:
        print_fn(f"  ... ({len(diff_lines)-80} more lines)")
    added   = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
    print_fn(f"─ {added} lines added, {removed} removed\n")

    approved = approval_fn(f"Edit {rel}: {instruction}", diff_lines[:20]) if approval_fn else False
    if not approved:
        print_fn("[EDIT] Cancelled.")
        return

    bak = path + "." + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
    shutil.copy2(path, bak)
    print_fn(f"[EDIT] Backup: {os.path.basename(bak)}")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        print_fn(f"[EDIT] ✓ Applied. Restart Umbra to load changes.\n")
        _chat_history.append({"role": "assistant", "content": f"Edited {rel}: {instruction}"})
    except Exception as e:
        print_fn(f"[EDIT] Write failed: {e}")
        shutil.copy2(bak, path)
        print_fn("[EDIT] Restored from backup.")


def handle_chat(message, print_fn=print):
    system = (
        "You are Umbra's internal dev assistant — a local, offline Claude-like AI "
        "built into Umbra OS (an autonomous AI runtime OS written in Python for Windows 11). "
        "Umbra uses Ollama for local LLMs, tkinter for GUI, pygame for games, PIL for images/GIFs. "
        "The main file is Umbra.py (~4200 lines). Key architecture: "
        "UmbraRuntimeKernel → UmbraRuntimeSpine → BossAgent → TaskEngine → GenerationEngine. "
        "When writing code, write complete working Python. "
        "Format code blocks with ``` markers. Be concise but complete."
    )
    _chat_history.append({"role": "user", "content": message})
    print_fn("\n[UMBRA] Thinking...\n")
    response = _ollama_chat(message, system=system, timeout=300)
    if not response:
        response = "I couldn't generate a response. Is Ollama running?"
    print_fn(response.strip())
    print_fn("")
    _chat_history.append({"role": "assistant", "content": response})


def handle_clear_history(print_fn=print):
    global _chat_history
    _chat_history = []
    print_fn("[DEV] Chat history cleared.\n")


def handle_which_model(print_fn=print):
    model = _pick_chat_model()
    print_fn(f"\n[DEV] Chat model: {model}")
    import urllib.request as _ur, json as _j
    try:
        with _ur.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            models = [m["name"] for m in _j.loads(r.read()).get("models", [])]
        print_fn(f"[DEV] Available: {', '.join(models)}")
    except Exception:
        print_fn("[DEV] Could not query Ollama.")
    print_fn("[DEV] For best results: ollama pull qwen3:14b\n")


# ── Main entry ────────────────────────────────────────────────────────────────

def process(user_input, print_fn=None, approval_fn=None):
    """
    Call from _process_command in Umbra.py.
    Returns True if handled (stop), False if not a dev command (pass through).
    """
    if print_fn is None:
        print_fn = print
    intent, args = detect_intent(user_input)
    if intent == "show_file":    handle_show_file(args["name"], args.get("start"), args.get("end"), print_fn); return True
    if intent == "edit_file":    handle_edit_file(args["name"], args.get("instruction",""), print_fn, approval_fn); return True
    if intent == "search_code":  handle_search_code(args["term"], args.get("scope"), print_fn); return True
    if intent == "list_files":   handle_list_files(print_fn); return True
    if intent == "run_tests":    handle_run_tests(print_fn); return True
    if intent == "clear_history":handle_clear_history(print_fn); return True
    if intent == "which_model":  handle_which_model(print_fn); return True
    if intent == "chat":         handle_chat(args["message"], print_fn); return True
    return False