import datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\.gitignore"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak33_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.py.bak.*
*.bak'''

NEW = '''# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.py.bak.*
*.bak
# Our actual apply_fixes backup naming (Umbra.py.bak22_20260630_221829, etc.)
# didn't match the two patterns above, so every batch's backup file was
# silently being committed. This catches the real pattern.
*.bak[0-9]*
*.bak_batch*'''

if OLD not in src:
    print("FAIL: anchor not found")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

OLD2 = '''# Large runtime/generated folders
workspaces/run_*/
workspaces/*/run_*/
workspaces/videos/
workspaces/*/generated/
workspaces/cache/'''

NEW2 = '''# Large runtime/generated folders
workspaces/run_*/
workspaces/*/run_*/
workspaces/videos/
workspaces/*/generated/
workspaces/cache/
# Generated test/full game builds and their project metadata, and
# generated images - these are local test output, not source, and
# bloat the repo (some via LFS) every time a game/image is built.
workspaces/agent_builds/
workspaces/projects/
workspaces/images/'''

if OLD2 not in src:
    print("FAIL: folders anchor not found")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

print("Fix applied: .gitignore now actually matches our backup/build-artifact naming (batch33)")