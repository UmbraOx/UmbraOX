import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak37_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Insert _run_smoke_test() function before _run_deep_build ---
OLD1 = '''
    return game_code, report


# ── 5. Full Pipeline Orchestrator ──────────────────────────
def _run_deep_build(runtime, description, project_name, agents_to_run=None):'''

NEW1 = '''
    return game_code, report


_SMOKE_HARNESS_SRC = r\'\'\'
import sys, os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import importlib.util
import pygame

GAME_PATH = sys.argv[1]
spec = importlib.util.spec_from_file_location("_umbra_smoke_game", GAME_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules["_umbra_smoke_game"] = mod

try:
    spec.loader.exec_module(mod)
except SystemExit:
    pass
except Exception as e:
    print("SMOKE_FAIL: import/top-level crash: " + repr(e))
    sys.exit(1)

pygame.init()
surf = pygame.Surface((1280, 720))
flex = getattr(mod, "_umbra_flex", lambda fn, *a, **kw: fn(*a, **kw))

try:
    if not hasattr(mod, "Player"):
        print("SMOKE_FAIL: no Player class found"); sys.exit(1)
    player = flex(mod.Player, "Warrior")

    if hasattr(mod, "Camera"):
        camera = flex(mod.Camera)
        flex(camera.update, player, 1280, 720)

    if hasattr(mod, "draw_main_menu"):
        r = mod.draw_main_menu(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_main_menu returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)

    if hasattr(mod, "draw_class_select"):
        r = mod.draw_class_select(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_class_select returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)

    if hasattr(mod, "spawn_world_entities"):
        enemies, npcs, buildings = mod.spawn_world_entities(
            getattr(mod, "WORLD_MAP", []), getattr(mod, "TOWNS", []),
            getattr(mod, "CITIES", []), getattr(mod, "BANDIT_CAMPS", [(0, 0)]),
            getattr(mod, "GOBLIN_CAMPS", [(0, 0)]), getattr(mod, "ENEMY_DEFS", {}))
        for e in (enemies or [])[:2]:
            flex(e.update, player, 0.016)
        for n in (npcs or [])[:2]:
            flex(n.update, 0.016)

except Exception as e:
    import traceback
    print("SMOKE_FAIL: " + repr(e))
    print(traceback.format_exc())
    sys.exit(1)

print("SMOKE_PASS")
sys.exit(0)
\'\'\'


def _run_smoke_test(game_path):
    """Headless post-build validation: imports the generated game and
    directly exercises the same contract call sites the real main() uses
    (Player/Camera construction, camera.update, draw_main_menu/
    draw_class_select, enemy spawn + update) in an isolated subprocess.
    Catches contract-mismatch crashes (the #1 cause of 'closes as soon as
    it opens') in about a second, instead of after a manual playthrough.
    Returns (passed: bool, output: str)."""
    import tempfile
    fd, harness_path = tempfile.mkstemp(suffix="_umbra_smoke.py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(_SMOKE_HARNESS_SRC)
        try:
            r = subprocess.run([sys.executable, harness_path, game_path],
                                capture_output=True, text=True, timeout=30)
            out = (r.stdout or "") + (r.stderr or "")
            passed = ("SMOKE_PASS" in out) and (r.returncode == 0)
            return passed, out
        except subprocess.TimeoutExpired:
            return False, "SMOKE_FAIL: harness timed out after 30s (possible infinite loop in setup)"
    finally:
        try:
            os.remove(harness_path)
        except Exception:
            pass


# ── 5. Full Pipeline Orchestrator ──────────────────────────
def _run_deep_build(runtime, description, project_name, agents_to_run=None):'''

if OLD1 not in src:
    print("FAIL: harness insertion anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: harness insertion anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Call the smoke test right after the game file is saved ---
OLD2 = '''    # ── Step 7: Save ───────────────────────────────────────
    game_path = os.path.join(proj_dir, proj_slug + "_game.py")
    with open(game_path, "w", encoding="utf-8") as f:
        f.write(game_code)

    total_lines = len(game_code.splitlines())'''

NEW2 = '''    # ── Step 7: Save ───────────────────────────────────────
    game_path = os.path.join(proj_dir, proj_slug + "_game.py")
    with open(game_path, "w", encoding="utf-8") as f:
        f.write(game_code)

    total_lines = len(game_code.splitlines())

    # ── Step 7b: Automated headless smoke test ──────────────
    _umbra_print("[UMBRA] Running automated smoke test (headless)...")
    _smoke_ok, _smoke_out = _run_smoke_test(game_path)
    if _smoke_ok:
        _umbra_print("[SMOKE TEST] PASS — Player/Camera/menu/class-select/spawn verified headlessly")
    else:
        _umbra_print("[SMOKE TEST] FAIL — found before you even launch it:")
        for _sl in _smoke_out.strip().splitlines()[-15:]:
            _umbra_print("    " + _sl)
        _umbra_print("[SMOKE TEST] Run 'fix last build' to attempt an automatic repair.")'''

if OLD2 not in src:
    print("FAIL: save-site anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: save-site anchor not unique")
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

print("Fix applied: automated headless smoke test runs after every build (batch37)")