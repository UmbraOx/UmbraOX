# apply_fixes_4.py — run from C:\Umbra: python apply_fixes_4.py
import ast, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()
fixes = []

# ── Fix 1: planner timeout 120→600 ──────────────────────────────────
old1 = 'raw = _ollama_stream(prompt, model=model, timeout=120, num_predict=400)'
new1 = 'raw = _ollama_stream(prompt, model=model, timeout=600, num_predict=400)'
if old1 in um:
    um = um.replace(old1, new1, 1); fixes.append("Fix 1 OK: planner timeout 120→600")
else:
    fixes.append("Fix 1 SKIP: already done")

# ── Fix 2: brief timeout 90→300 ─────────────────────────────────────
old2 = 'model=model, timeout=90, num_predict=160'
new2 = 'model=model, timeout=300, num_predict=160'
if old2 in um:
    um = um.replace(old2, new2, 1); fixes.append("Fix 2 OK: brief timeout 90→300")
else:
    fixes.append("Fix 2 SKIP: already done")

# ── Fix 3: auto-patch existing game files before launch ─────────────
MENU_PATCH = '''
# UMBRA_MENU_PATCH
try:
    _omm = draw_main_menu
    def draw_main_menu(surf, project_name=''):
        result = _omm(surf, project_name)
        if isinstance(result, dict): return result
        import pygame as _pg2
        W,H = surf.get_size()
        keys = ['new_game','load_game','settings','quit','start','play','continue','exit']
        if isinstance(result, (list, tuple)):
            out = {}
            for i,item in enumerate(result):
                k = keys[i] if i < len(keys) else 'btn_'+str(i)
                if isinstance(item, _pg2.Rect): out[k] = item
                elif isinstance(item, tuple) and len(item)==2 and isinstance(item[1],_pg2.Rect): out[k] = item[1]
            return out if out else {'new_game':_pg2.Rect(W//2-100,H//2-20,200,40)}
        return {'new_game':_pg2.Rect(W//2-100,H//2-20,200,40)}
except Exception: pass
'''

# Find the launch block and add auto-patch before Popen
old3 = (
    '            _umbra_print("[UMBRA] Launching: " + game_path)\n'
    '            try:\n'
    '                subprocess.Popen([sys.executable, game_path], cwd=os.path.dirname(game_path))\n'
    '            except Exception as e:\n'
    '                _umbra_print("  Error: " + str(e))'
)
new3 = (
    '            # Auto-patch existing game files before launch\n'
    '            try:\n'
    '                _gsrc = open(game_path, "r", encoding="utf-8").read()\n'
    '                if "UMBRA_MENU_PATCH" not in _gsrc and "draw_main_menu" in _gsrc:\n'
    '                    _gsrc += ' + repr(MENU_PATCH) + '\n'
    '                    open(game_path, "w", encoding="utf-8").write(_gsrc)\n'
    '            except Exception: pass\n'
    '            _umbra_print("[UMBRA] Launching: " + game_path)\n'
    '            try:\n'
    '                subprocess.Popen([sys.executable, game_path], cwd=os.path.dirname(game_path))\n'
    '            except Exception as e:\n'
    '                _umbra_print("  Error: " + str(e))'
)
if old3 in um:
    um = um.replace(old3, new3, 1); fixes.append("Fix 3 OK: auto-patch game on launch")
else:
    fixes.append("Fix 3 SKIP: launch block not found")

open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)

for f in fixes:
    print(f)

try:
    ast.parse(um)
    print("\nSyntax OK")
except SyntaxError as e:
    print(f"\nSYNTAX ERROR: {e}")