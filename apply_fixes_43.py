import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak43_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    if hasattr(mod, "spawn_world_entities"):
        enemies, npcs, buildings = mod.spawn_world_entities(
            getattr(mod, "WORLD_MAP", []), getattr(mod, "TOWNS", []),
            getattr(mod, "CITIES", []), getattr(mod, "BANDIT_CAMPS", [(0, 0)]),
            getattr(mod, "GOBLIN_CAMPS", [(0, 0)]), getattr(mod, "ENEMY_DEFS", {}))
        for e in (enemies or [])[:2]:
            flex(e.update, player, 0.016)
        for n in (npcs or [])[:2]:
            flex(n.update, 0.016)'''

NEW = '''    if hasattr(mod, "spawn_world_entities"):
        enemies, npcs, buildings = mod.spawn_world_entities(
            getattr(mod, "WORLD_MAP", []), getattr(mod, "TOWNS", []),
            getattr(mod, "CITIES", []), getattr(mod, "BANDIT_CAMPS", [(0, 0)]),
            getattr(mod, "GOBLIN_CAMPS", [(0, 0)]), getattr(mod, "ENEMY_DEFS", {}))
        # Exercise both update() and draw() - missing draw() (agent defines
        # an entity class but never gives it a way to render itself) is
        # just as fatal as a missing update() once main()'s draw loop
        # reaches it, and was slipping through untested before.
        for e in (enemies or [])[:2]:
            flex(e.update, player, 0.016)
            if not hasattr(e, "draw"):
                print("SMOKE_FAIL: Enemy instance has no draw() method")
                sys.exit(1)
            flex(e.draw, surf, 0, 0)
        for n in (npcs or [])[:2]:
            flex(n.update, 0.016)
            if not hasattr(n, "draw"):
                print("SMOKE_FAIL: NPC instance has no draw() method")
                sys.exit(1)
            flex(n.draw, surf, 0, 0)
        for b in (buildings or [])[:2]:
            if not hasattr(b, "draw"):
                print("SMOKE_FAIL: Building instance has no draw() method")
                sys.exit(1)
            flex(b.draw, surf, 0, 0)'''

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

print("Fix applied: smoke test now exercises .draw() for enemies/npcs/buildings too (batch43)")