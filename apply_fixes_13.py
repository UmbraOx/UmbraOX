import subprocess, glob, os

content = """[pytest]
addopts = -q
testpaths = . core/tests core/runtime tests
norecursedirs = sandbox _deleted_tests_backup_* venv .git __pycache__
"""

with open("pytest.ini", "w", encoding="utf-8") as f:
    f.write(content)
print("Created pytest.ini with norecursedirs for sandbox/backup folders")

# untrack (but keep locally) the backup folder
backup_dirs = glob.glob("_deleted_tests_backup_*")
for d in backup_dirs:
    r = subprocess.run(f'git rm -r --cached "{d}"', shell=True, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)

# add to .gitignore
gi_line = "_deleted_tests_backup_*/\n"
existing = ""
if os.path.exists(".gitignore"):
    with open(".gitignore", "r", encoding="utf-8") as f:
        existing = f.read()
if gi_line.strip() not in existing:
    with open(".gitignore", "a", encoding="utf-8") as f:
        f.write(gi_line)
    print("Added backup dir pattern to .gitignore")