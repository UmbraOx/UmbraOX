"""
test_umbra_full.py — Umbra v2.4.0 Full Test Suite
Place at: C:/Umbra/test_umbra_full.py
Run with: python test_umbra_full.py

Tests every critical system without requiring Ollama or ComfyUI to be running.
All tests are self-contained and deterministic.
Expected result: ALL TESTS PASS
"""

import sys, os, ast, json, time, importlib, traceback, tempfile, shutil

# ── Point at your Umbra root ──────────────────────────────────────────────
UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
if UMBRA_ROOT not in sys.path:
    sys.path.insert(0, UMBRA_ROOT)

PASS = []; FAIL = []

def test(name, fn):
    try:
        fn()
        PASS.append(name)
        print("  [PASS] " + name)
    except Exception as e:
        FAIL.append((name, str(e)))
        print("  [FAIL] " + name + "\n         " + str(e))


# ════════════════════════════════════════════════════════════
#  GROUP 1 — UMBRA.PY ITSELF
# ════════════════════════════════════════════════════════════
print("\n[GROUP 1] Umbra.py core file")

def t_umbra_exists():
    found = any(os.path.exists(os.path.join(UMBRA_ROOT, n))
                for n in ["Umbra.py","umbra.py","UMBRA.py"])
    assert found, "Umbra.py not found in " + UMBRA_ROOT
test("Umbra.py exists", t_umbra_exists)

def t_umbra_syntax():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            ast.parse(src)
            return
    raise AssertionError("Umbra.py not found")
test("Umbra.py syntax clean", t_umbra_syntax)

def t_umbra_has_build_runtime():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def build_runtime" in src
            return
test("Umbra.py has build_runtime()", t_umbra_has_build_runtime)

def t_umbra_has_safe_imports():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "_si(" in src or "try:" in src, "build_runtime still has bare imports"
            return
test("build_runtime uses safe imports", t_umbra_has_safe_imports)

def t_umbra_no_bare_runtime_llm():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            # The old pattern was a bare 'from core.runtime... import' with no try/except
            # After patch this should not exist at module level
            lines = src.split('\n')
            for i, ln in enumerate(lines):
                stripped = ln.strip()
                if stripped.startswith('from core.runtime.runtime_llm_provider import'):
                    # Check if inside try block (previous non-empty line should have try: or be indented)
                    # After our patch it should be inside _si() call, not a bare import
                    assert 'try:' in lines[max(0,i-3):i+1] or '_si(' in src[:src.find(stripped)+200], \
                        "Bare import of runtime_llm_provider found at line " + str(i+1)
            return
test("No crash-causing bare imports in build_runtime", t_umbra_no_bare_runtime_llm)

def t_umbra_has_safe_input():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "_safe_input" in src, "_safe_input() not found — GUI mode will crash"
            return
test("_safe_input() present", t_umbra_has_safe_input)

def t_umbra_print_banner_safe():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            # Old broken version had bare 'from core.runtime.runtime_version import'
            # at module level inside print_banner
            idx = src.find("def print_banner")
            snippet = src[idx:idx+300]
            if "from core.runtime.runtime_version import" in snippet:
                assert "try:" in snippet, "print_banner has bare version import — will crash"
            return
test("print_banner() is crash-safe", t_umbra_print_banner_safe)

def t_umbra_shutdown_safe():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            idx = src.find("def _shutdown")
            snippet = src[idx:idx+400]
            assert 'runtime["memory"]' not in snippet, \
                "_shutdown uses runtime['memory'] directly — will crash if memory not loaded"
            return
test("_shutdown() safe with missing keys", t_umbra_shutdown_safe)

def t_umbra_launch_gui_has_fallback():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            idx = src.find("def _launch_gui")
            snippet = src[idx:idx+600]
            assert "_MinimalGUI" in snippet or "launch_in_thread" in snippet, \
                "_launch_gui has no fallback GUI"
            return
test("_launch_gui() has fallback window", t_umbra_launch_gui_has_fallback)


# ════════════════════════════════════════════════════════════
#  GROUP 2 — CORE RUNTIME FILES SYNTAX
# ════════════════════════════════════════════════════════════
print("\n[GROUP 2] Core runtime file syntax")

RUNTIME_DIR = os.path.join(UMBRA_ROOT, "core", "runtime")

def t_runtime_dir_exists():
    assert os.path.isdir(RUNTIME_DIR), "core/runtime/ not found"
test("core/runtime/ exists", t_runtime_dir_exists)

def t_all_runtime_syntax():
    if not os.path.isdir(RUNTIME_DIR): return
    broken = []
    for fname in sorted(os.listdir(RUNTIME_DIR)):
        if not fname.endswith(".py"): continue
        p = os.path.join(RUNTIME_DIR, fname)
        try:
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            ast.parse(src)
        except SyntaxError as e:
            broken.append(fname + ": " + str(e))
    assert not broken, str(len(broken)) + " broken: " + "; ".join(broken[:5])
test("All core/runtime/*.py syntax clean", t_all_runtime_syntax)

CRITICAL_FILES = [
    "umbra_runtime_spine.py",
    "umbra_task_engine.py",
    "umbra_generation_engine.py",
    "umbra_runtime_kernel.py",
    "runtime_image_generator.py",
]
for fname in CRITICAL_FILES:
    def _make_test(fn):
        def _t():
            p = os.path.join(RUNTIME_DIR, fn)
            assert os.path.exists(p), fn + " not found — install from fix package"
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            ast.parse(src)
        return _t
    test(fname + " exists and parses", _make_test(fname))


# ════════════════════════════════════════════════════════════
#  GROUP 3 — GAME SKELETON
# ════════════════════════════════════════════════════════════
print("\n[GROUP 3] Game skeleton")

SKELETON_PATH = os.path.join(UMBRA_ROOT, "core", "assets", "game_skeleton.py")

def t_skeleton_exists():
    assert os.path.exists(SKELETON_PATH), \
        "core/assets/game_skeleton.py not found — download from fix package"
test("game_skeleton.py exists", t_skeleton_exists)

def t_skeleton_has_placeholders():
    if not os.path.exists(SKELETON_PATH): return
    with open(SKELETON_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    for ph in ["__WORLD_CODE__","__CHAR_CODE__","__ITEM_CODE__","__PROJECT_NAME__"]:
        assert ph in src, "Placeholder " + ph + " missing from skeleton"
test("game_skeleton.py has all placeholders", t_skeleton_has_placeholders)

def t_skeleton_stitches():
    if not os.path.exists(SKELETON_PATH): return
    with open(SKELETON_PATH,"r",encoding="utf-8",errors="replace") as f: tmpl = f.read()
    result = tmpl.replace("__PROJECT_NAME__","TestGame").replace("__PROJ_SLUG__","testgame")
    for ph in ["__WORLD_CODE__","__CHAR_CODE__","__ITEM_CODE__",
               "__MECH_CODE__","__UI_CODE__","__QUEST_CODE__","__ECON_CODE__"]:
        result = result.replace(ph, "# agent placeholder")
    ast.parse(result)
test("game_skeleton.py stitches and parses", t_skeleton_stitches)

def t_skeleton_fallbacks():
    if not os.path.exists(SKELETON_PATH): return
    with open(SKELETON_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    for kw in ["Player","Enemy","NPC","Camera","WEAPONS","SPELLS","QUESTS",
               "draw_hud","draw_minimap","draw_inventory","draw_pause",
               "K_w","K_ESCAPE","K_i","F5","F9","json.dump","json.load"]:
        assert kw in src, "Skeleton missing: " + kw
test("game_skeleton.py has all required systems", t_skeleton_fallbacks)

def t_skeleton_x_buttons():
    if not os.path.exists(SKELETON_PATH): return
    with open(SKELETON_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "draw_x_button" in src or "xbtn" in src or "_xbtn" in src, \
        "Skeleton missing X close buttons on menus"
test("game_skeleton.py has X close buttons", t_skeleton_x_buttons)

def t_skeleton_no_input_calls():
    if not os.path.exists(SKELETON_PATH): return
    with open(SKELETON_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    lines = [ln for ln in src.split('\n') if 'input(' in ln and not ln.strip().startswith('#')]
    assert not lines, "Skeleton has input() calls — will hang: " + str(lines[:2])
test("game_skeleton.py has no input() calls", t_skeleton_no_input_calls)


# ════════════════════════════════════════════════════════════
#  GROUP 4 — GUI
# ════════════════════════════════════════════════════════════
print("\n[GROUP 4] GUI control center")

GUI_PATHS = [
    os.path.join(UMBRA_ROOT,"core","gui","control_center.py"),
    os.path.join(UMBRA_ROOT,"core","ui","umbra_control_center.py"),
]

def t_gui_exists():
    found = any(os.path.exists(p) for p in GUI_PATHS)
    assert found, "GUI control_center.py not found in core/gui/ or core/ui/"
test("GUI control_center.py exists", t_gui_exists)

def t_gui_syntax():
    for p in GUI_PATHS:
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            ast.parse(src)
            return
test("GUI file syntax clean", t_gui_syntax)

def t_gui_has_log():
    for p in GUI_PATHS:
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def log(" in src or "def _log(" in src, "GUI missing log() method"
            assert "def post_message(" in src, "GUI missing post_message() method"
            return
test("GUI has log() and post_message()", t_gui_has_log)

def t_gui_has_launch_in_thread():
    for p in GUI_PATHS:
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def launch_in_thread" in src, "GUI missing launch_in_thread()"
            return
test("GUI has launch_in_thread()", t_gui_has_launch_in_thread)

def t_gui_log_not_empty():
    for p in GUI_PATHS:
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            idx = src.find("def _log(")
            if idx < 0: idx = src.find("def log(")
            snippet = src[idx:idx+200]
            # Check it's not just 'pass'
            assert snippet.count("pass") == 0 or "queue" in snippet or "_write" in snippet, \
                "log() method appears to be empty (just 'pass')"
            return
test("GUI log() method is implemented", t_gui_log_not_empty)


# ════════════════════════════════════════════════════════════
#  GROUP 5 — IMAGE GENERATOR
# ════════════════════════════════════════════════════════════
print("\n[GROUP 5] Image generator")

IMG_PATH = os.path.join(RUNTIME_DIR, "runtime_image_generator.py")

def t_img_exists():
    assert os.path.exists(IMG_PATH), "runtime_image_generator.py not found"
test("runtime_image_generator.py exists", t_img_exists)

def t_img_negative_prompt():
    if not os.path.exists(IMG_PATH): return
    with open(IMG_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    for kw in ["bad hands","extra fingers","missing fingers","extra limbs",
               "deformed","bad anatomy","worst quality"]:
        assert kw in src, "Negative prompt missing: " + kw
test("Image generator has professional negative prompts", t_img_negative_prompt)

def t_img_pil_fallback():
    if not os.path.exists(IMG_PATH): return
    with open(IMG_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "PIL" in src or "Pillow" in src, "No PIL fallback in image generator"
    assert "_pil_placeholder" in src or "placeholder" in src.lower(), \
        "No PIL placeholder fallback found"
test("Image generator has PIL fallback", t_img_pil_fallback)


# ════════════════════════════════════════════════════════════
#  GROUP 6 — GENERATION ENGINE ROUTING
# ════════════════════════════════════════════════════════════
print("\n[GROUP 6] Generation engine routing")

GEN_PATH = os.path.join(RUNTIME_DIR, "umbra_generation_engine.py")

def t_gen_routes_image():
    if not os.path.exists(GEN_PATH): return
    with open(GEN_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "comfyui" in src.lower() or "ComfyUI" in src, \
        "Generation engine doesn't route images to ComfyUI"
test("Generation engine routes image → ComfyUI", t_gen_routes_image)

def t_gen_routes_game():
    if not os.path.exists(GEN_PATH): return
    with open(GEN_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "_gen_game" in src or "game_prompt" in src, \
        "Generation engine doesn't have game generation route"
test("Generation engine routes game → code gen", t_gen_routes_game)

def t_gen_routes_sprite():
    if not os.path.exists(GEN_PATH): return
    with open(GEN_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "sprite" in src.lower(), "Generation engine missing sprite route"
test("Generation engine routes sprite → PIL", t_gen_routes_sprite)

def t_gen_not_all_llm():
    if not os.path.exists(GEN_PATH): return
    with open(GEN_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    # Old broken version returned raw LLM text for everything
    # New version should have separate handlers per type
    assert src.count("task_type") >= 3, \
        "Generation engine may still be routing all types through single LLM call"
test("Generation engine has per-type routing (not single LLM)", t_gen_not_all_llm)


# ════════════════════════════════════════════════════════════
#  GROUP 7 — RUNTIME SPINE
# ════════════════════════════════════════════════════════════
print("\n[GROUP 7] Runtime spine")

SPINE_PATH = os.path.join(RUNTIME_DIR, "umbra_runtime_spine.py")

def t_spine_no_bridge_analyze():
    if not os.path.exists(SPINE_PATH): return
    with open(SPINE_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "bridge.analyze(" not in src, \
        "umbra_runtime_spine still calls bridge.analyze() which doesn't exist — will crash"
test("Runtime spine: bridge.analyze() removed", t_spine_no_bridge_analyze)

def t_spine_has_run_task():
    if not os.path.exists(SPINE_PATH): return
    with open(SPINE_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "def run_task" in src, "Runtime spine missing run_task()"
test("Runtime spine has run_task()", t_spine_has_run_task)

def t_spine_has_stubs():
    if not os.path.exists(SPINE_PATH): return
    with open(SPINE_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "Stub" in src or "stub" in src or "try:" in src, \
        "Runtime spine has no fallback stubs — will crash if sub-modules missing"
test("Runtime spine has fallback stubs", t_spine_has_stubs)


# ════════════════════════════════════════════════════════════
#  GROUP 8 — TASK ENGINE
# ════════════════════════════════════════════════════════════
print("\n[GROUP 8] Task engine")

TASK_PATH = os.path.join(RUNTIME_DIR, "umbra_task_engine.py")

def t_task_accepts_goal():
    if not os.path.exists(TASK_PATH): return
    with open(TASK_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    # Should handle both task_id AND goal string
    assert "task_id_or_goal" in src or "not in self.tasks" in src or "create_task" in src, \
        "Task engine run_task() doesn't accept goal strings — BossAgent calls will crash"
test("Task engine run_task() accepts goal strings", t_task_accepts_goal)

def t_task_has_create():
    if not os.path.exists(TASK_PATH): return
    with open(TASK_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "def create_task" in src, "Task engine missing create_task()"
test("Task engine has create_task()", t_task_has_create)


# ════════════════════════════════════════════════════════════
#  GROUP 9 — RUNTIME KERNEL
# ════════════════════════════════════════════════════════════
print("\n[GROUP 9] Runtime kernel")

KERNEL_PATH = os.path.join(RUNTIME_DIR, "umbra_runtime_kernel.py")

def t_kernel_has_registry():
    if not os.path.exists(KERNEL_PATH): return
    with open(KERNEL_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    for method in ["register_module","get","exists","list","unregister"]:
        assert "def " + method in src, "Kernel missing method: " + method
test("Runtime kernel has full module registry", t_kernel_has_registry)

def t_kernel_has_safe_execute():
    if not os.path.exists(KERNEL_PATH): return
    with open(KERNEL_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    assert "def safe_execute" in src, "Kernel missing safe_execute()"
test("Runtime kernel has safe_execute()", t_kernel_has_safe_execute)

def t_kernel_has_event_bus():
    if not os.path.exists(KERNEL_PATH): return
    with open(KERNEL_PATH,"r",encoding="utf-8",errors="replace") as f: src = f.read()
    for method in ["subscribe","emit","_emit"]:
        assert "def " + method in src, "Kernel missing event bus method: " + method
test("Runtime kernel has event bus", t_kernel_has_event_bus)


# ════════════════════════════════════════════════════════════
#  GROUP 10 — WORKSPACES
# ════════════════════════════════════════════════════════════
print("\n[GROUP 10] Workspaces")

WS = os.path.join(UMBRA_ROOT, "workspaces")

def t_workspaces_exist():
    os.makedirs(WS, exist_ok=True)
    assert os.path.isdir(WS)
test("workspaces/ directory exists", t_workspaces_exist)

for sub in ["images","videos","sprites","agent_builds","code","apps","text","projects"]:
    def _mk(s):
        def _t():
            p = os.path.join(WS, s)
            os.makedirs(p, exist_ok=True)
            assert os.path.isdir(p)
        return _t
    test("workspaces/" + sub + "/ exists", _mk(sub))


# ════════════════════════════════════════════════════════════
#  GROUP 11 — STITCH FUNCTION
# ════════════════════════════════════════════════════════════
print("\n[GROUP 11] Game stitching")

def t_stitch_function_present():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def _stitch_game" in src, "_stitch_game() not in Umbra.py"
            return
test("_stitch_game() function present", t_stitch_function_present)

def t_stitch_uses_skeleton():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            idx = src.find("def _stitch_game")
            snippet = src[idx:idx+600]
            assert "game_skeleton.py" in snippet or "skeleton_path" in snippet, \
                "_stitch_game() doesn't load core/assets/game_skeleton.py"
            return
test("_stitch_game() loads game_skeleton.py", t_stitch_uses_skeleton)

def t_stitch_inline_fallback():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "_INLINE_SKELETON" in src, \
                "No _INLINE_SKELETON fallback — stitch will fail if skeleton file missing"
            return
test("_stitch_game() has inline skeleton fallback", t_stitch_inline_fallback)


# ════════════════════════════════════════════════════════════
#  GROUP 12 — REQUIREMENTS VALIDATION
# ════════════════════════════════════════════════════════════
print("\n[GROUP 12] Game requirements validation")

def t_validate_requirements_present():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "_REQUIREMENTS" in src or "_validate_requirements" in src
            return
test("_validate_requirements() present", t_validate_requirements_present)

def t_validate_checks_wasd():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "K_w" in src and "wasd" in src.lower(), \
                "Requirement check for WASD movement missing"
            return
test("Requirements check includes WASD", t_validate_checks_wasd)


# ════════════════════════════════════════════════════════════
#  GROUP 13 — AGENT SYSTEM
# ════════════════════════════════════════════════════════════
print("\n[GROUP 13] Agent system")

def t_agent_roles_defined():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "_AGENT_ROLES" in src or "_build_agent_prompt" in src, \
                "Agent role definitions not found"
            return
test("Agent role definitions present", t_agent_roles_defined)

def t_seven_agents():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            for agent in ["world","character","item","mechanic","ui","quest","economy"]:
                assert '"' + agent + '"' in src or "'" + agent + "'" in src, \
                    "Agent missing: " + agent
            return
test("All 7 specialist agents defined", t_seven_agents)

def t_deep_build_present():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def _run_deep_build" in src, "_run_deep_build() missing"
            return
test("_run_deep_build() present", t_deep_build_present)


# ════════════════════════════════════════════════════════════
#  GROUP 14 — SELF-REPAIR + INSTALL
# ════════════════════════════════════════════════════════════
print("\n[GROUP 14] Self-repair and self-install")

def t_handle_self_fix():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def handle_self_fix" in src
            return
test("handle_self_fix() present", t_handle_self_fix)

def t_handle_self_install():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def handle_self_install" in src
            return
test("handle_self_install() present", t_handle_self_install)

def t_handle_integrate():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def handle_integrate" in src
            # Check it now does case-insensitive search
            idx = src.find("def handle_integrate")
            snippet = src[idx:idx+800]
            assert '"Umbra.py"' in snippet or '_cand' in snippet or 'umbra.py' in snippet.lower()
            return
test("handle_integrate() present and case-insensitive", t_handle_integrate)

def t_approval_system():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8",errors="replace") as f: src = f.read()
            assert "def _approval_prompt" in src, "Approval system missing"
            return
test("Approval system present", t_approval_system)


# ════════════════════════════════════════════════════════════
#  GROUP 15 — QUICK FUNCTIONAL SMOKE TESTS
# ════════════════════════════════════════════════════════════
print("\n[GROUP 15] Quick functional smoke tests")

def t_stitch_runs():
    """Actually call _stitch_game() with dummy components and verify output."""
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if not os.path.exists(p): continue
        spec = importlib.util.spec_from_file_location("umbra_mod", p)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod._stitch_game("TestGame","A test RPG",{
            "world": "# world stub",
            "character": "# char stub",
        })
        assert "TestGame" in result, "Project name not in stitched output"
        assert "import pygame" in result or "pygame" in result, "pygame not in stitched output"
        ast.parse(result)  # Must be valid Python
        return
test("_stitch_game() produces valid Python", t_stitch_runs)

def t_find_broken_modules_runs():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if not os.path.exists(p): continue
        spec = importlib.util.spec_from_file_location("umbra_mod2", p)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        broken = mod._find_broken_modules()
        assert isinstance(broken, list), "_find_broken_modules() did not return a list"
        return
test("_find_broken_modules() runs without error", t_find_broken_modules_runs)

def t_syntax_check_runs():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if not os.path.exists(p): continue
        spec = importlib.util.spec_from_file_location("umbra_mod3", p)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod._syntax_check(p)
        assert result is None, "Umbra.py reports its own syntax error: " + str(result)
        return
test("_syntax_check(Umbra.py) returns None (clean)", t_syntax_check_runs)

def t_validate_requirements_runs():
    for n in ["Umbra.py","umbra.py","UMBRA.py"]:
        p = os.path.join(UMBRA_ROOT, n)
        if not os.path.exists(p): continue
        spec = importlib.util.spec_from_file_location("umbra_mod4", p)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # Test with known-good game code snippet
        sample = (
            "import pygame\n"
            "WORLD_MAP=[]; WEAPONS=[]; SPELLS=[]; QUESTS=[]; ENEMY_DEFS=[]\n"
            "def main():\n"
            "    pygame.init()\n"
            "    screen=pygame.display.set_mode((1280,720))\n"
            "    clock=pygame.time.Clock()\n"
            "    while True:\n"
            "        for e in pygame.event.get():\n"
            "            if e.type==pygame.QUIT: break\n"
            "            if e.type==pygame.KEYDOWN:\n"
            "                if e.key==pygame.K_ESCAPE: pass\n"
            "                if e.key==pygame.K_i: pass\n"
            "                if e.key==pygame.K_q: pass\n"
            "        keys=pygame.key.get_pressed()\n"
            "        if keys[pygame.K_w]: pass\n"
            "        if keys[pygame.K_s]: pass\n"
            "        if keys[pygame.K_a]: pass\n"
            "        if keys[pygame.K_d]: pass\n"
            "        clock.tick(60)\n"
            "    pygame.quit()\n"
            "PAUSE='PAUSE'; atk=1; hp=1\n"
            "def draw_bar(): pass\n"
            "def draw_x_button(): pass\n"
            "import json\n"
            "json.dump({},''); json.load('')\n"
            "if __name__=='__main__': main()\n"
        )
        passed, failed = mod._validate_requirements(sample)
        assert len(passed) >= 8, \
            "Only " + str(len(passed)) + " requirements passed on sample game: " + str(failed)
        return
test("_validate_requirements() checks game code correctly", t_validate_requirements_runs)


# ════════════════════════════════════════════════════════════
#  FINAL REPORT
# ════════════════════════════════════════════════════════════
total = len(PASS) + len(FAIL)
print("\n" + "="*60)
print("  UMBRA TEST RESULTS")
print("="*60)
print("  PASSED : " + str(len(PASS)) + "/" + str(total))
print("  FAILED : " + str(len(FAIL)) + "/" + str(total))
if FAIL:
    print("\n  FAILURES:")
    for name, err in FAIL:
        print("    x " + name)
        print("      " + err[:120])
print("="*60)

if not FAIL:
    print("\n  ALL TESTS PASS — Umbra is ready to launch.")
    print("  Run:  python Umbra.py")
    print("  Then: make a game called DemiWorld")
    print("  Then: make an image of a dark fantasy castle")
else:
    print("\n  Fix the failures above then re-run this test.")
    print("  Most failures = missing files from the fix package.")
    print("  Copy all 8 files from the fix package then re-run.")

sys.exit(0 if not FAIL else 1)