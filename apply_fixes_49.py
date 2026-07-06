import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak49_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Store smoke-test status keyed by game path right after it runs ---
OLD1 = '''    else:
        _umbra_print("[SMOKE TEST] FAIL — found before you even launch it:")
        for _sl in _smoke_out.strip().splitlines()[-15:]:
            _umbra_print("    " + _sl)
        _umbra_print("[SMOKE TEST] Run 'fix last build' to attempt an automatic repair.")

    if pm:'''

NEW1 = '''    else:
        _umbra_print("[SMOKE TEST] FAIL — found before you even launch it:")
        for _sl in _smoke_out.strip().splitlines()[-15:]:
            _umbra_print("    " + _sl)
        _umbra_print("[SMOKE TEST] Run 'fix last build' to attempt an automatic repair.")

    # Remember this build's smoke-test result so 'play last'/'play <name>'
    # can refuse to launch a build we already know is broken, instead of
    # the warning above being easy to miss and the game just closing anyway.
    try:
        _smoke_status_path = os.path.join(_UMBRA_ROOT, "sessions", "smoke_status.json")
        _smoke_status = {}
        if os.path.exists(_smoke_status_path):
            try:
                _smoke_status = json.load(open(_smoke_status_path, "r", encoding="utf-8"))
            except Exception:
                _smoke_status = {}
        _smoke_status[game_path] = {
            "ok": _smoke_ok,
            "summary": _smoke_out.strip().splitlines()[-1] if _smoke_out.strip() else "",
        }
        os.makedirs(os.path.dirname(_smoke_status_path), exist_ok=True)
        json.dump(_smoke_status, open(_smoke_status_path, "w", encoding="utf-8"))
    except Exception:
        pass

    if pm:'''

if OLD1 not in src:
    print("FAIL: smoke-status-store anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: smoke-status-store anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Check status + require explicit override at the play-last launch site ---
OLD2 = '''        if game_path and os.path.exists(game_path):
            # Auto-patch game: fix draw_main_menu to return dict not list'''

NEW2 = '''        if game_path and os.path.exists(game_path):
            # Refuse to launch a build we already know failed its smoke
            # test, unless the person explicitly overrides - the warning
            # printed at build time is easy to miss/scroll past, and this
            # was letting people relaunch a build we'd already told them
            # was broken.
            _allow_broken = cmd.endswith(" anyway")
            try:
                _sstatus_path = os.path.join(_UMBRA_ROOT, "sessions", "smoke_status.json")
                if os.path.exists(_sstatus_path) and not _allow_broken:
                    _sstatus = json.load(open(_sstatus_path, "r", encoding="utf-8"))
                    _entry = _sstatus.get(game_path)
                    if _entry and not _entry.get("ok", True):
                        _umbra_print("[UMBRA] NOT launching - this build already failed its smoke test:")
                        _umbra_print("    " + _entry.get("summary", "(no details saved)"))
                        _umbra_print("[UMBRA] Type 'fix last build' to repair it, or '" + cmd + " anyway' to launch it as-is.")
                        return
            except Exception:
                pass
            # Auto-patch game: fix draw_main_menu to return dict not list'''

if OLD2 not in src:
    print("FAIL: play-last launch anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: play-last launch anchor not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: play-last refuses a known-failed build unless overridden with 'anyway' (batch49)")