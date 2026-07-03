import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak31_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''            _SKELETON_FUNS = {"main","run_game","game_loop","game_main","start_game","run",
                              "txt","draw_text","render_text","draw_main_menu","draw_menu"}'''

NEW = '''            # These are "contract" functions: main()'s event loop unpacks their
            # return value into a specific shape (dict of named rects, or a
            # fixed-arity tuple). If an agent redefines one with a different
            # return shape (e.g. a list instead of a dict), main() crashes the
            # instant that screen is used. Always strip agent versions so the
            # skeleton's own contract-safe implementations govern.
            _SKELETON_FUNS = {"main","run_game","game_loop","game_main","start_game","run",
                              "txt","draw_text","render_text","draw_main_menu","draw_menu",
                              "draw_hud","draw_bar","draw_panel","draw_inventory","draw_shop",
                              "draw_pause","draw_class_select","draw_crafting","draw_city_build",
                              "draw_world_map","draw_dialogue","draw_gameover"}'''

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

print("Fix applied: strip agent overrides of all UI contract functions (batch31)")