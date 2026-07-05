import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak47_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''        for b in (buildings or [])[:2]:
            if not hasattr(b, "draw"):
                print("SMOKE_FAIL: Building instance has no draw() method")
                sys.exit(1)
            flex(b.draw, surf, 0, 0)

except Exception as e:'''

NEW = '''        for b in (buildings or [])[:2]:
            if not hasattr(b, "draw"):
                print("SMOKE_FAIL: Building instance has no draw() method")
                sys.exit(1)
            flex(b.draw, surf, 0, 0)

    # Exercise draw_world across a spread of camera positions, including
    # ones near map edges/corners - this is exactly the gap that let a
    # None-cell/out-of-bounds WORLD_MAP crash through untested before.
    if hasattr(mod, "draw_world"):
        for _cx, _cy in [(0, 0), (5000, 5000), (-100, -100), (99999, 99999)]:
            mod.draw_world(surf, _cx, _cy)

except Exception as e:'''

if OLD not in src:
    print("FAIL: anchor not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: smoke test exercises draw_world across camera positions incl. edges (batch47)")