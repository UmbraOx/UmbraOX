# fix_menu_final.py — run from C:\Umbra: python fix_menu_final.py
import ast, os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Fix 1: Umbra.py — add draw_main_menu to skeleton strip list ──────
um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()
old = '            _SKELETON_FUNS = {"main","run_game","game_loop","game_main","start_game","run",\n                              "txt","draw_text","render_text"}'
new = '            _SKELETON_FUNS = {"main","run_game","game_loop","game_main","start_game","run",\n                              "txt","draw_text","render_text","draw_main_menu","draw_menu"}'
if old in um:
    um = um.replace(old, new, 1)
    open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)
    ast.parse(um)
    print("Fix 1 OK: draw_main_menu protected from agent override")
else:
    print("Fix 1 SKIP: already applied")

# ── Fix 2: patch all existing game files with wrapper ────────────────
PATCH = '''
# UMBRA_MENU_DICT_PATCH
try:
    _omm2 = draw_main_menu
    def draw_main_menu(surf, project_name=''):
        import pygame as _pg
        result = _omm2(surf, project_name) if _omm2.__code__.co_varcount > 1 else _omm2(surf)
        if isinstance(result, dict): return result
        W, H = surf.get_size()
        KEYS = ['new_game','continue','quit','settings','load_game','credits']
        if isinstance(result, (list, tuple)):
            out = {}
            for i, item in enumerate(result):
                k = KEYS[i] if i < len(KEYS) else 'btn_' + str(i)
                if isinstance(item, _pg.Rect):
                    out[k] = item
                elif isinstance(item, (list, tuple)) and item:
                    r = next((x for x in item if isinstance(x, _pg.Rect)), None)
                    if r: out[k] = r
            if out: return out
        return {'new_game': _pg.Rect(W//2-120, H//2, 240, 50),
                'continue': _pg.Rect(W//2-120, H//2+70, 240, 50),
                'quit':     _pg.Rect(W//2-120, H//2+140, 240, 50)}
except Exception:
    pass
'''

games = glob.glob(os.path.join(ROOT, 'workspaces', 'agent_builds', '**', '*_game.py'), recursive=True)
for gp in games:
    src = open(gp, encoding='utf-8').read()
    if 'UMBRA_MENU_DICT_PATCH' in src:
        print(f"SKIP (already patched): {os.path.basename(gp)}")
        continue
    src2 = src + PATCH
    try:
        ast.parse(src2)
        open(gp, 'w', encoding='utf-8').write(src2)
        print(f"Fix 2 OK: patched {os.path.basename(gp)}")
    except SyntaxError as e:
        print(f"Fix 2 ERROR on {os.path.basename(gp)}: {e}")

print("\nDone. Run:")
print("  git add -A && git commit -m 'Fix draw_main_menu override' && git push origin main")
print("  python Umbra.py")
print("  play last  (or build a new game)")