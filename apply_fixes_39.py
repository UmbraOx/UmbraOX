import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak39_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''try:
    if not hasattr(mod, "Player"):
        print("SMOKE_FAIL: no Player class found"); sys.exit(1)
    player = flex(mod.Player, "Warrior")

    if hasattr(mod, "Camera"):
        camera = flex(mod.Camera)
        flex(camera.update, player, 1280, 720)

    if hasattr(mod, "draw_main_menu"):
        r = mod.draw_main_menu(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_main_menu returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)

    if hasattr(mod, "draw_class_select"):
        r = mod.draw_class_select(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_class_select returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)'''

NEW = '''try:
    if not hasattr(mod, "Player"):
        print("SMOKE_FAIL: no Player class found"); sys.exit(1)
    player = flex(mod.Player, "Warrior")

    if hasattr(mod, "Camera"):
        camera = flex(mod.Camera)
        flex(camera.update, player, 1280, 720)

    if hasattr(mod, "draw_main_menu"):
        r = mod.draw_main_menu(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_main_menu returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)

    class_labels = []
    if hasattr(mod, "draw_class_select"):
        r = mod.draw_class_select(surf)
        if not isinstance(r, dict):
            print("SMOKE_FAIL: draw_class_select returned " + type(r).__name__ + ", expected dict")
            sys.exit(1)
        class_labels = list(r.keys())

    # Actually construct a Player for every class-select button label, not
    # just a hardcoded "Warrior" - this is exactly the gap that let a
    # class-name-validation crash through: the class-select screen offered
    # a label the agent's own Player.__init__ didn't recognize.
    for _cls_label in class_labels:
        try:
            flex(mod.Player, _cls_label)
        except Exception as e:
            print("SMOKE_FAIL: Player(" + repr(_cls_label) +
                  ") crashed - class-select button doesn't match Player's "
                  "accepted classes: " + repr(e))
            sys.exit(1)'''

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

print("Fix applied: smoke test now checks Player() against every class-select label (batch39)")