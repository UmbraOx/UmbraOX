# apply_fixes_5.py — run from C:\Umbra: python apply_fixes_5.py
import ast, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Fix 1: patch Umbra.py launch block ──────────────────────────────
um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()

old = (
    '            # Auto-patch existing game files before launch\n'
    '            try:\n'
    '                _gsrc = open(game_path, "r", encoding="utf-8").read()\n'
    '                if "UMBRA_MENU_PATCH" not in _gsrc and "draw_main_menu" in _gsrc:\n'
)
new = (
    '            # Auto-patch game: fix draw_main_menu to return dict not list\n'
    '            try:\n'
    '                import re as _rp, ast as _ast2\n'
    '                _gsrc = open(game_path, "r", encoding="utf-8").read()\n'
    '                _MENU_KEYS = ["new_game","continue","load_game","settings","quit","credits"]\n'
    '                def _fix_menu_ret(code):\n'
    '                    lines = code.splitlines()\n'
    '                    in_menu = False\n'
    '                    out = []\n'
    '                    for ln in lines:\n'
    '                        if ln.startswith("def draw_main_menu"): in_menu = True\n'
    '                        elif ln.startswith("def ") and in_menu: in_menu = False\n'
    '                        if in_menu and ln.strip().startswith("return [") and ln.strip().endswith("]"):\n'
    '                            items = [x.strip() for x in ln.strip()[8:-1].split(",")]\n'
    '                            pairs = ", ".join(f\'"{_MENU_KEYS[i] if i<len(_MENU_KEYS) else "btn_"+str(i)}":{v}\' for i,v in enumerate(items))\n'
    '                            ln = "    return {" + pairs + "}"\n'
    '                        out.append(ln)\n'
    '                    return "\\n".join(out)\n'
    '                _gsrc2 = _fix_menu_ret(_gsrc)\n'
    '                if _gsrc2 != _gsrc:\n'
    '                    _ast2.parse(_gsrc2)\n'
    '                    open(game_path, "w", encoding="utf-8").write(_gsrc2)\n'
    '                if "UMBRA_MENU_PATCH" not in _gsrc:\n'
)

if old in um:
    um = um.replace(old, new, 1)
    open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)
    try:
        ast.parse(um)
        print("Fix 1 OK: smart menu auto-patch on launch")
    except SyntaxError as e:
        print(f"Fix 1 SYNTAX ERROR: {e}")
else:
    print("Fix 1 SKIP: already applied")

# ── Fix 2: directly patch the existing game file on disk ─────────────
game_path = os.path.join(ROOT, 'workspaces', 'agent_builds', 'mygame', 'mygame_game.py')
if os.path.exists(game_path):
    gsrc = open(game_path, encoding='utf-8').read()
    lines = gsrc.splitlines()
    in_menu = False
    changed = False
    out = []
    KEYS = ["new_game", "continue", "load_game", "settings", "quit", "credits"]
    for ln in lines:
        if ln.startswith("def draw_main_menu"): in_menu = True
        elif ln.startswith("def ") and in_menu: in_menu = False
        if in_menu and ln.strip().startswith("return [") and ln.strip().endswith("]"):
            items = [x.strip() for x in ln.strip()[8:-1].split(",")]
            pairs = ", ".join(f'"{KEYS[i] if i < len(KEYS) else "btn_"+str(i)}": {v}' for i, v in enumerate(items))
            ln = "    return {" + pairs + "}"
            changed = True
        out.append(ln)
    if changed:
        fixed = "\n".join(out)
        try:
            ast.parse(fixed)
            open(game_path, 'w', encoding='utf-8').write(fixed)
            print("Fix 2 OK: patched game file on disk")
        except SyntaxError as e:
            print(f"Fix 2 SYNTAX ERROR in game file: {e}")
    else:
        print("Fix 2 SKIP: game file already returns dict or not found")
else:
    print("Fix 2 SKIP: no game file on disk yet")

print("\nDone. Run: git add -A && git commit -m 'Fix menu returns dict' && git push origin main && python Umbra.py")
print("Then type: play last")