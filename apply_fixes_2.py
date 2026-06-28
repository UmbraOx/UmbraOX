# apply_fixes_2.py — run from C:\Umbra with: python apply_fixes_2.py
import ast, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()

# ── Fix 1: play last — only scan agent_builds for *_game.py ─────────
old1 = (
    '        if not game_path:\n'
    '            ws_base = os.path.join(_UMBRA_ROOT, "workspaces")\n'
    '            candidates = []\n'
    '            for root, dirs, files in os.walk(ws_base):\n'
    '                dirs[:] = [d for d in dirs if d not in ("__pycache__",".git")]\n'
    '                for fname in files:\n'
    '                    if not fname.endswith(".py"): continue\n'
    '                    full = os.path.join(root, fname)\n'
    '                    try: mtime = os.path.getmtime(full)\n'
    '                    except: continue\n'
    '                    score = mtime\n'
    '                    if any(g in fname.lower() for g in ["game","optiopia","demiworld","myworld","rpg"]): score += 1e12\n'
    '                    if project_name and project_name.lower() in full.lower(): score += 2e12\n'
    '                    if fname in ("main.py","__init__.py") and "game" not in fname.lower(): score -= 1e10\n'
    '                    candidates.append((score, full))'
)
new1 = (
    '        if not game_path:\n'
    '            # Only look in agent_builds for *_game.py files\n'
    '            ws_base = os.path.join(_UMBRA_ROOT, "workspaces", "agent_builds")\n'
    '            candidates = []\n'
    '            if os.path.isdir(ws_base):\n'
    '                for root, dirs, files in os.walk(ws_base):\n'
    '                    dirs[:] = [d for d in dirs if d not in ("__pycache__",".git")]\n'
    '                    for fname in files:\n'
    '                        if not fname.endswith("_game.py"): continue\n'
    '                        full = os.path.join(root, fname)\n'
    '                        try: mtime = os.path.getmtime(full)\n'
    '                        except: continue\n'
    '                        score = mtime\n'
    '                        if project_name and project_name.lower() in full.lower(): score += 2e12\n'
    '                        candidates.append((score, full))'
)
if old1 in um:
    um = um.replace(old1, new1, 1)
    print("Fix 1 OK: play last only scans agent_builds/*_game.py")
else:
    print("Fix 1 SKIP: not found")

# ── Fix 2: delete broken old mygame so it stops being launched ───────
old_game = os.path.join(ROOT, 'workspaces', 'agent_builds', 'mygame', 'mygame_game.py')
if os.path.exists(old_game):
    os.remove(old_game)
    print("Fix 2 OK: deleted stale mygame_game.py")
else:
    print("Fix 2 SKIP: mygame_game.py not found")

# ── Write and verify ─────────────────────────────────────────────────
open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)
try:
    ast.parse(um)
    print("\nSyntax OK")
    print("Run: git add -A && git commit -m 'Fix play last routing, delete stale game' && git push origin main")
    print("Then: python Umbra.py")
    print("Then type: build optiopia")
    print("Then type: play last")
except SyntaxError as e:
    print(f"\nSYNTAX ERROR: {e}")