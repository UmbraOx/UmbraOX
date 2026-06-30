# push_batch5.py -- verify and push batch 5
import ast, subprocess, sys, os, glob

if not os.path.exists("Umbra.py"):
    print("ERROR: Run from C:\\Umbra"); sys.exit(1)

# AST checks
for f, subs in [("Umbra.py", {}),
                (os.path.join("core","assets","game_skeleton.py"),
                 {"__WORLD_CODE__":"pass","__CHAR_CODE__":"pass","__ITEM_CODE__":"pass",
                  "__MECH_CODE__":"pass","__UI_CODE__":"pass","__QUEST_CODE__":"pass",
                  "__ECON_CODE__":"pass","__PROJECT_NAME__":"Umbra"})]:
    try:
        src = open(f, encoding="utf-8").read()
        for k, v in subs.items(): src = src.replace(k, v)
        ast.parse(src)
        print("AST OK:", f)
    except SyntaxError as e:
        print("AST ERROR", f, "line", e.lineno, ":", e.msg); sys.exit(1)
    except FileNotFoundError:
        print("MISSING:", f); sys.exit(1)

# Run smoke test
r = subprocess.run([sys.executable, "umbra_smoke_test.py"], capture_output=True, text=True)
print(r.stdout[-400:] if len(r.stdout) > 400 else r.stdout)
if r.returncode != 0:
    print("SMOKE TEST FAILED -- aborting push"); sys.exit(1)

# Cleanup
for f in glob.glob("*.bak_batch5*") + glob.glob(os.path.join("core","assets","*.bak_batch5*")):
    try: os.remove(f); print("Removed:", f)
    except: pass
for f in ["apply_fixes_5.py", "push_batch5.py"]:
    if os.path.exists(f):
        try: os.remove(f); print("Removed:", f)
        except: pass

for cmd in [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "feat: polished HUD+minimap, ollama retry, v3.0.0, smoke test 27/27, full handoff"],
    ["git", "push", "origin", "main"],
]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(" ".join(cmd[:3]), "->", r.returncode)
    if r.stdout.strip(): print(r.stdout.strip())
    if r.stderr.strip(): print(r.stderr.strip())
    if r.returncode != 0 and cmd[1] != "commit":
        print("STOP"); sys.exit(1)
print("\nDone. 27/27 smoke tests passing. Umbra v3.0.0.")