import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\core\assets\game_skeleton.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak53_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD1 = '''            if best.hp <= 0:
                best.alive = False
                check_quest_kill(player, best.name)
                done = complete_ready_quests(player)'''

NEW1 = '''            if best.hp <= 0:
                best.alive = False
                # check_quest_kill/complete_ready_quests are plain
                # functions (usually quest-agent authored), not object
                # methods, so they can't be monkey-patched with a
                # constructor safety net like Player/Enemy - wrap the
                # call site itself instead.
                try:
                    check_quest_kill(player, best.name)
                except Exception:
                    pass
                try:
                    done = complete_ready_quests(player)
                except Exception:
                    done = []'''

if OLD1 not in src:
    print("FAIL: first check_quest_kill site not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: first check_quest_kill site not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

OLD2 = '''                            if e.hp <= 0:
                                e.alive = False
                                check_quest_kill(player, e.name)
                                player.gain_xp(e.xp_val)
                                player.gold += e.gold_drop'''

NEW2 = '''                            if e.hp <= 0:
                                e.alive = False
                                try:
                                    check_quest_kill(player, e.name)
                                except Exception:
                                    pass
                                player.gain_xp(e.xp_val)
                                player.gold += e.gold_drop'''

if OLD2 not in src:
    print("FAIL: second check_quest_kill site not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: second check_quest_kill site not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

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

print("Fix applied: check_quest_kill/complete_ready_quests call sites wrapped defensively (batch53)")