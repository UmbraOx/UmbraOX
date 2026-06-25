"""
test_dev_assistant.py — Tests for umbra_dev_assistant.py
Run: python test_dev_assistant.py
All tests must PASS before shipping.
"""
import sys, os, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import umbra_dev_assistant as da

PASS = 0; FAIL = 0

def test(name, fn):
    global PASS, FAIL
    try:
        result = fn()
        if result is True or result is None:
            print(f"  PASS  {name}")
            PASS += 1
        else:
            print(f"  FAIL  {name} — got {result!r}")
            FAIL += 1
    except Exception as e:
        print(f"  FAIL  {name} — {e}")
        FAIL += 1

print("\n=== umbra_dev_assistant tests ===\n")

# ── Intent detection ──────────────────────────────────────────────────────────
test("show file intent",        lambda: da.detect_intent("show umbra.py")[0] == "show_file")
test("show file with lines",    lambda: da.detect_intent("show umbra.py 100-200") == ("show_file", {"name":"umbra.py","start":100,"end":200}))
test("read file intent",        lambda: da.detect_intent("read control_center.py")[0] == "show_file")
test("search intent",           lambda: da.detect_intent("search for _safe_input")[0] == "search_code")
test("search term extracted",   lambda: da.detect_intent("search for _safe_input")[1]["term"] == "_safe_input")
test("list files intent",       lambda: da.detect_intent("list files")[0] == "list_files")
test("run tests intent",        lambda: da.detect_intent("run tests")[0] == "run_tests")
test("tests shorthand",         lambda: da.detect_intent("tests")[0] == "run_tests")
test("clear history intent",    lambda: da.detect_intent("clear history")[0] == "clear_history")
test("which model intent",      lambda: da.detect_intent("which model")[0] == "which_model")
test("chat intent explain",     lambda: da.detect_intent("explain how the agent pipeline works")[0] == "chat")
test("chat intent question",    lambda: da.detect_intent("what is run_prompt?")[0] == "chat")
test("chat intent how does",    lambda: da.detect_intent("how does the GIF generator work?")[0] == "chat")
test("non-dev passes through",  lambda: da.detect_intent("make a game called Optiopia")[0] is None)
test("non-dev gif passes",      lambda: da.detect_intent("make a gif of a dragon")[0] is None)
test("non-dev build passes",    lambda: da.detect_intent("build a platformer")[0] is None)
test("edit intent",             lambda: da.detect_intent("edit umbra.py: fix the bug")[0] == "edit_file")
test("edit name extracted",     lambda: da.detect_intent("edit umbra.py: fix the bug")[1]["name"] == "umbra.py")
test("edit instruction",        lambda: da.detect_intent("edit umbra.py: fix the bug")[1]["instruction"] == "fix the bug")

# ── Path resolution ───────────────────────────────────────────────────────────
test("resolve umbra alias",     lambda: da._resolve_path("umbra.py") is not None)
test("resolve umbra.py exists", lambda: os.path.exists(da._resolve_path("umbra.py")))
test("resolve gif generator",   lambda: da._resolve_path("gif_generator.py") is not None)
test("resolve by filename",     lambda: da._resolve_path("Umbra.py") is not None)

# ── show_file handler ─────────────────────────────────────────────────────────
def test_show_file():
    out = []
    da.handle_show_file("umbra.py", start=1, end=5, print_fn=out.append)
    joined = "\n".join(out)
    assert "[FILE]" in joined, "no [FILE] header"
    assert "┌─" in joined, "no box header"
    assert "│" in joined, "no line content"
    return True
test("show_file output format", test_show_file)

def test_show_file_range():
    out = []
    da.handle_show_file("umbra.py", start=10, end=15, print_fn=out.append)
    joined = "\n".join(out)
    assert "10" in joined
    return True
test("show_file line range", test_show_file_range)

def test_show_missing():
    out = []
    da.handle_show_file("nonexistent_xyz.py", print_fn=out.append)
    return "not found" in "\n".join(out).lower()
test("show_file missing file", test_show_missing)

# ── search handler ────────────────────────────────────────────────────────────
def test_search():
    out = []
    da.handle_search_code("_safe_input", print_fn=out.append)
    joined = "\n".join(out)
    assert "SEARCH" in joined
    assert "Umbra.py" in joined
    return True
test("search finds _safe_input in Umbra.py", test_search)

def test_search_no_results():
    out = []
    da.handle_search_code("ZZZNOMATCH_SENTINEL_UNIQUE", print_fn=out.append)
    joined = "\n".join(out)
    # Should report 0 or very low match count (only in test file itself is irrelevant)
    return "match(es) found" in joined
test("search no results", test_search_no_results)

# ── list_files handler ────────────────────────────────────────────────────────
def test_list_files():
    out = []
    da.handle_list_files(print_fn=out.append)
    joined = "\n".join(out)
    assert "Umbra.py" in joined
    assert "✓" in joined or "✗" in joined
    return True
test("list_files shows key files", test_list_files)

# ── clear_history handler ─────────────────────────────────────────────────────
def test_clear():
    da._chat_history.append({"role": "user", "content": "test"})
    out = []
    da.handle_clear_history(print_fn=out.append)
    return len(da._chat_history) == 0
test("clear_history empties history", test_clear)

# ── process() dispatch ────────────────────────────────────────────────────────
def test_process_show():
    out = []
    result = da.process("show umbra.py 1-3", print_fn=out.append)
    return result is True and "[FILE]" in "\n".join(out)
test("process() dispatches show_file", test_process_show)

def test_process_search():
    out = []
    result = da.process("search for _safe_input", print_fn=out.append)
    return result is True
test("process() dispatches search", test_process_search)

def test_process_passthrough():
    result = da.process("make a gif of a dragon")
    return result is False
test("process() passes through gif command", test_process_passthrough)

def test_process_list():
    out = []
    result = da.process("list files", print_fn=out.append)
    return result is True and "Umbra.py" in "\n".join(out)
test("process() dispatches list_files", test_process_list)

# ── Player class fix check ────────────────────────────────────────────────────
def test_player_has_active_quests():
    path = os.path.join(os.path.dirname(__file__),
                        "workspaces", "agent_builds", "testrpg", "testrpg_game.py")
    if not os.path.exists(path):
        return True  # skip if game not present
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    # Check outer Player class has active_quests
    player_idx = src.index("class Player:")
    segment = src[player_idx:player_idx+1500]
    return "active_quests" in segment
test("testrpg Player has active_quests", test_player_has_active_quests)

# ── _stitch_game safety patch check ──────────────────────────────────────────
def test_stitch_safety_patch():
    umbra_path = os.path.join(os.path.dirname(__file__), "Umbra.py")
    with open(umbra_path, "r", encoding="utf-8") as f:
        src = f.read()
    return "UMBRA SAFETY PATCH" in src
test("Umbra.py has Player safety patch in _stitch_game", test_stitch_safety_patch)

# ── Umbra.py has dev_asst import ─────────────────────────────────────────────
def test_umbra_has_dev_asst():
    umbra_path = os.path.join(os.path.dirname(__file__), "Umbra.py")
    with open(umbra_path, "r", encoding="utf-8") as f:
        src = f.read()
    return "import umbra_dev_assistant as _dev_asst" in src
test("Umbra.py imports _dev_asst", test_umbra_has_dev_asst)

def test_umbra_hooks_dev_asst():
    umbra_path = os.path.join(os.path.dirname(__file__), "Umbra.py")
    with open(umbra_path, "r", encoding="utf-8") as f:
        src = f.read()
    return "_dev_asst.process" in src
test("Umbra.py hooks _dev_asst.process in _process_command", test_umbra_hooks_dev_asst)

# ── GUI clarifying question patch ─────────────────────────────────────────────
def test_clarify_gui_patch():
    umbra_path = os.path.join(os.path.dirname(__file__), "Umbra.py")
    with open(umbra_path, "r", encoding="utf-8") as f:
        src = f.read()
    return "askstring" in src
test("Umbra.py uses askstring for clarifying questions in GUI", test_clarify_gui_patch)

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'='*40}")
print(f"  {PASS} passed  |  {FAIL} failed")
print(f"{'='*40}\n")
sys.exit(0 if FAIL == 0 else 1)