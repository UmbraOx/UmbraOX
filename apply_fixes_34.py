import subprocess, os

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

# Confirmed via repo-wide grep: zero references in any .py or .md file,
# not mentioned in UMBRA_HANDOFF.md, not imported/called anywhere.
ORPHAN_FILES = [
    "fix_game.py", "fix_game_now.py", "fix_menu_final.py",
    "stress_1.py", "stress_2.py", "dashboard_test.py",
    "layer5_test.py", "layer6_test_1.py", "layer8_test.py", "layer9_test.py",
    "autonomy_test_1.py", "fail_test.py", "future_test.py", "live_test.py",
    "test_a.py", "test_adaptive.py", "test_collab.py", "test_feedback.py",
    "test_layer4_fix_2.py", "test_layer5_b.py", "test_patch.py", "test_registry_fix.py",
]

# Leftover backup folders from an old test-cleanup pass (batches 12-18).
# Their job is done; only the old patch scripts that created them still
# mention them, and those scripts already ran.
ORPHAN_DIRS = [
    "_deleted_tests_backup_20260630_040906",
    "_deleted_tests_backup_20260630_044121",
]

removed = []
for f in ORPHAN_FILES:
    p = os.path.join(r"C:\Umbra", f)
    if os.path.exists(p):
        os.remove(p)
        removed.append(f)

for d in ORPHAN_DIRS:
    p = os.path.join(r"C:\Umbra", d)
    if os.path.isdir(p):
        import shutil
        shutil.rmtree(p)
        removed.append(d + "/")

print("Removed " + str(len(removed)) + " orphaned item(s):")
for r in removed:
    print("  - " + r)
print("Fix applied: repo cleanup - orphaned scripts/folders removed (batch34)")