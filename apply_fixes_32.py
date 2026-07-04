import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\core\assets\game_skeleton.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak32_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. imports + generic adaptive-call helper ---
OLD1 = '''import pygame
import sys
import math
import random
import json
import os
import time
'''

NEW1 = '''import pygame
import sys
import math
import random
import json
import os
import time
import inspect

# ─── Adaptive contract calling ──────────────────────────────────────────
# Agent-authored classes (Player, Camera, Enemy, NPC, ...) sometimes have
# constructors/methods with a different arity than what this skeleton
# calls with (e.g. Camera.update(self, player) instead of
# Camera.update(self, player, sw, sh)). That mismatch used to be an
# instant TypeError crash the moment the game reached that call. This
# wrapper inspects the real target's signature and adapts: trims extra
# positional args the target doesn't accept, and fills any additional
# *required* params the agent's version added with a sensible default
# guessed from the parameter name. It only changes behavior when the
# plain call would have raised a TypeError.
def _umbra_flex(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except TypeError:
        pass
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        raise
    params = [p for p in sig.parameters.values()
              if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                             inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL
                       for p in sig.parameters.values())
    max_pos = len(params) if not has_varargs else len(args)
    call_args = list(args[:max_pos])
    for i in range(len(call_args), min(max_pos, len(params))):
        p = params[i]
        if p.default is not inspect.Parameter.empty:
            break
        nl = p.name.lower()
        if nl in ("sw", "screen_w", "width", "w"):
            call_args.append(1280)
        elif nl in ("sh", "screen_h", "height", "h"):
            call_args.append(720)
        elif nl in ("dt", "delta", "delta_time"):
            call_args.append(0.016)
        elif "name" in nl:
            call_args.append("Entity")
        elif nl in ("cls", "class_name", "player_class", "job"):
            call_args.append("Warrior")
        elif nl in ("x", "y", "ex", "ey", "nx", "ny"):
            call_args.append(0)
        else:
            call_args.append(None)
    return fn(*call_args, **kwargs)
'''

if OLD1 not in src:
    print("FAIL: imports anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: imports anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Wrap Enemy/NPC construction inside fallback spawn_world_entities ---
OLD2 = '''                enemies.append(Enemy("Bandit",ex,ey))
                ei+=1'''
NEW2 = '''                enemies.append(_umbra_flex(Enemy, "Bandit", ex, ey))
                ei+=1'''
if OLD2 not in src:
    print("FAIL: Enemy Bandit site not found"); sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: Enemy Bandit site not unique"); sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

OLD3 = '''                enemies.append(Enemy("Goblin",ex,ey))'''
NEW3 = '''                enemies.append(_umbra_flex(Enemy, "Goblin", ex, ey))'''
if OLD3 not in src:
    print("FAIL: Enemy Goblin site not found"); sys.exit(1)
if src.count(OLD3) != 1:
    print("FAIL: Enemy Goblin site not unique"); sys.exit(1)
src = src.replace(OLD3, NEW3, 1)

OLD4 = '''                npcs.append(NPC(name, nx, ny, job))'''
NEW4 = '''                npcs.append(_umbra_flex(NPC, name, nx, ny, job))'''
if OLD4 not in src:
    print("FAIL: NPC site not found"); sys.exit(1)
if src.count(OLD4) != 1:
    print("FAIL: NPC site not unique"); sys.exit(1)
src = src.replace(OLD4, NEW4, 1)

# --- 3. Wrap Player/Camera construction ---
OLD5 = '''    player    = Player("Warrior")
    player_ref = player   # used by draw_dialogue for quest acceptance
    camera    = Camera()'''
NEW5 = '''    player    = _umbra_flex(Player, "Warrior")
    player_ref = player   # used by draw_dialogue for quest acceptance
    camera    = _umbra_flex(Camera)'''
if OLD5 not in src:
    print("FAIL: Player/Camera construction site not found"); sys.exit(1)
if src.count(OLD5) != 1:
    print("FAIL: Player/Camera construction site not unique"); sys.exit(1)
src = src.replace(OLD5, NEW5, 1)

# --- 4. Wrap Player(cls) at class-select ---
OLD6 = '''                            player = Player(cls)'''
NEW6 = '''                            player = _umbra_flex(Player, cls)'''
if OLD6 not in src:
    print("FAIL: Player(cls) site not found"); sys.exit(1)
if src.count(OLD6) != 1:
    print("FAIL: Player(cls) site not unique"); sys.exit(1)
src = src.replace(OLD6, NEW6, 1)

# --- 5. Wrap per-frame update() calls ---
OLD7 = '''            camera.update(player, SCREEN_W, SCREEN_H)

            for e in enemies:
                e.update(player, dt)'''
NEW7 = '''            _umbra_flex(camera.update, player, SCREEN_W, SCREEN_H)

            for e in enemies:
                _umbra_flex(e.update, player, dt)'''
if OLD7 not in src:
    print("FAIL: camera/enemy update site not found"); sys.exit(1)
if src.count(OLD7) != 1:
    print("FAIL: camera/enemy update site not unique"); sys.exit(1)
src = src.replace(OLD7, NEW7, 1)

OLD8 = '''            for p in projectiles:
                p.update(dt)'''
NEW8 = '''            for p in projectiles:
                _umbra_flex(p.update, dt)'''
if OLD8 not in src:
    print("FAIL: projectile update site not found"); sys.exit(1)
if src.count(OLD8) != 1:
    print("FAIL: projectile update site not unique"); sys.exit(1)
src = src.replace(OLD8, NEW8, 1)

OLD9 = '''            for ft in float_texts:
                ft.update(dt)'''
NEW9 = '''            for ft in float_texts:
                _umbra_flex(ft.update, dt)'''
if OLD9 not in src:
    print("FAIL: float_text update site not found"); sys.exit(1)
if src.count(OLD9) != 1:
    print("FAIL: float_text update site not unique"); sys.exit(1)
src = src.replace(OLD9, NEW9, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

test_src = (src.replace("__WORLD_CODE__", "").replace("__CHAR_CODE__", "")
               .replace("__ITEM_CODE__", "").replace("__MECH_CODE__", "")
               .replace("__UI_CODE__", "").replace("__QUEST_CODE__", "")
               .replace("__ECON_CODE__", "").replace("__PROJECT_NAME__", "TestGame")
               .replace("__PROJ_SLUG__", "testgame"))
try:
    ast.parse(test_src)
    print("game_skeleton.py AST OK (with placeholders substituted)")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: adaptive signature-safe calling for all agent-class contract sites (batch32)")