# fix_game.py — run from C:\Umbra: python fix_game.py
import ast, os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
KEYS = ["new_game", "continue", "load_game", "settings", "quit", "credits"]

def fix_game_file(path):
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines()
    in_menu = False
    changed = False
    out = []
    for ln in lines:
        if ln.startswith("def draw_main_menu"): in_menu = True
        elif ln.startswith("def ") and in_menu: in_menu = False
        if in_menu and ln.strip().startswith("return [") and ln.strip().endswith("]"):
            items = [x.strip() for x in ln.strip()[8:-1].split(",")]
            pairs = ", ".join(f'"{KEYS[i] if i<len(KEYS) else "btn_"+str(i)}": {v}' for i,v in enumerate(items))
            ln = "    return {" + pairs + "}"
            changed = True
        out.append(ln)
    if changed:
        fixed = "\n".join(out)
        try:
            ast.parse(fixed)
            open(path, 'w', encoding='utf-8').write(fixed)
            print(f"FIXED: {path}")
        except SyntaxError as e:
            print(f"SYNTAX ERROR: {e}")
    else:
        print(f"SKIP (no list return found): {os.path.basename(path)}")

# Fix all game files
for gf in glob.glob(os.path.join(ROOT, 'workspaces', 'agent_builds', '**', '*_game.py'), recursive=True):
    fix_game_file(gf)

print("Done — run: python Umbra.py then: play last")