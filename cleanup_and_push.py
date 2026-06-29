# cleanup_and_push.py -- delete .bak and old apply_fixes files, then git push
# Run from C:\Umbra:  python cleanup_and_push.py
import os, subprocess, glob, sys

ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "Umbra.py")):
    print("ERROR: Run from C:\\Umbra"); sys.exit(1)

# Delete .bak files
removed = []
for f in glob.glob("Umbra.py.bak*") + glob.glob("*.bak_*"):
    try: os.remove(f); removed.append(f)
    except: pass

# Delete old numbered apply_fixes (keep apply_fixes_2.py and cleanup_and_push.py)
for f in ["apply_fixes.py","apply_fixes_2.py","apply_fixes_3.py","apply_fixes_4.py","apply_fixes_5.py",
          "apply_fixes_1.py","apply_fixes_1b.py"]:
    if os.path.exists(f):
        try: os.remove(f); removed.append(f)
        except: pass

if removed:
    print("Removed:", removed)
else:
    print("Nothing to remove.")

# Verify AST still OK
import ast
src = open("Umbra.py", encoding="utf-8").read()
try:
    ast.parse(src)
    print("AST OK")
except SyntaxError as e:
    print("AST ERROR line", e.lineno, ":", e.msg); sys.exit(1)

# Git push
cmds = [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "fix: agent AST retry, snake routing, voice auto-install, project name extraction, cleanup"],
    ["git", "push", "origin", "main"],
]
for cmd in cmds:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(" ".join(cmd[:3]), "->", r.returncode)
    if r.stdout.strip(): print(r.stdout.strip())
    if r.stderr.strip(): print(r.stderr.strip())
    if r.returncode != 0 and cmd[1] != "commit":
        print("STOP: command failed"); sys.exit(1)

print("\nDone.")