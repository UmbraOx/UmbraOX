import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_and_read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        s = f.read()
    with open(fp + f".bak46_{ts}", "w", encoding="utf-8") as f:
        f.write(s)
    return s

# --- 1. Umbra.py: add UMBRA_WORLD_PATCH alongside the existing patches ---
FP1 = r"C:\Umbra\Umbra.py"
src1 = backup_and_read(FP1)

OLD1 = '''            if _cn in ('Enemy','NPC','Projectile','Building') and not hasattr(_cls,'draw'):
                _cls.draw = _umbra_fallback_draw
except Exception:
    pass
\'\'\''''

NEW1 = '''            if _cn in ('Enemy','NPC','Projectile','Building') and not hasattr(_cls,'draw'):
                _cls.draw = _umbra_fallback_draw
except Exception:
    pass
# UMBRA_WORLD_PATCH
# WORLD_MAP and its accessor (get_biome/get_tile) are entirely agent-authored
# whenever the agent supplies its own WORLD_MAP (the skeleton's own safe
# fallback - which bounds-checks and never has None cells - only runs if
# 'WORLD_MAP' isn't already in globals). An agent's WORLD_MAP can have gaps
# (None cells) or its accessor can index without bounds-checking, crashing
# draw_world() the instant the camera reaches that tile. Patch this the same
# way as the Player/Enemy fixes above: wrap whatever accessor exists so it
# can never return None or raise, and scrub any None cells already present.
try:
    for _bn in ('get_biome', 'get_tile'):
        if _bn in dir():
            _orig_biome_fn = eval(_bn)
            def _umbra_make_safe_biome(_fn):
                def _safe_biome(*a, **kw):
                    try:
                        _r = _fn(*a, **kw)
                        return _r if _r is not None else "GRASS"
                    except Exception:
                        return "GRASS"
                return _safe_biome
            globals()[_bn] = _umbra_make_safe_biome(_orig_biome_fn)
    if 'WORLD_MAP' in dir() and isinstance(WORLD_MAP, list):
        for _wrow in WORLD_MAP:
            if isinstance(_wrow, list):
                for _wi in range(len(_wrow)):
                    if _wrow[_wi] is None:
                        _wrow[_wi] = "GRASS"
except Exception:
    pass
\'\'\''''

if OLD1 not in src1:
    print("FAIL: UMBRA_WORLD_PATCH anchor not found")
    sys.exit(1)
if src1.count(OLD1) != 1:
    print("FAIL: UMBRA_WORLD_PATCH anchor not unique")
    sys.exit(1)
src1 = src1.replace(OLD1, NEW1, 1)

with open(FP1, "w", encoding="utf-8") as f:
    f.write(src1)

try:
    ast.parse(src1)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL (Umbra.py): " + str(e))
    sys.exit(1)

# --- 2. game_skeleton.py: wrap the draw_world call site defensively ---
FP2 = r"C:\Umbra\core\assets\game_skeleton.py"
src2 = backup_and_read(FP2)

OLD2 = '''            # World
            draw_world(screen, int(camera.x), int(camera.y))'''

NEW2 = '''            # World
            # A crash inside draw_world (e.g. an agent's WORLD_MAP accessor
            # returning/indexing None for a tile it didn't generate) used to
            # take down the entire game the instant the camera reached that
            # tile. UMBRA_WORLD_PATCH fixes the accessor itself when
            # possible; this is the last-resort net: skip rendering the
            # world for this one frame rather than crashing outright.
            try:
                draw_world(screen, int(camera.x), int(camera.y))
            except Exception:
                pass'''

if OLD2 not in src2:
    print("FAIL: draw_world call-site anchor not found")
    sys.exit(1)
if src2.count(OLD2) != 1:
    print("FAIL: draw_world call-site anchor not unique")
    sys.exit(1)
src2 = src2.replace(OLD2, NEW2, 1)

with open(FP2, "w", encoding="utf-8") as f:
    f.write(src2)

test_src = (src2.replace("__WORLD_CODE__", "").replace("__CHAR_CODE__", "")
                .replace("__ITEM_CODE__", "").replace("__MECH_CODE__", "")
                .replace("__UI_CODE__", "").replace("__QUEST_CODE__", "")
                .replace("__ECON_CODE__", "").replace("__PROJECT_NAME__", "TestGame")
                .replace("__PROJ_SLUG__", "testgame"))
try:
    ast.parse(test_src)
    print("game_skeleton.py AST OK (with placeholders substituted)")
except SyntaxError as e:
    print("AST FAIL (game_skeleton.py): " + str(e))
    sys.exit(1)

print("Fix applied: world-map get_biome/get_tile safety patch + draw_world call-site net (batch46)")