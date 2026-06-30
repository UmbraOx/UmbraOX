import subprocess, sys, glob, os

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(1)

# Clean clutter: bak files and old apply_fixes/push_batch scripts (keep this batch's pair)
for pattern in ["*.bak_batch*", "apply_fixes_*.py", "push_batch*.py", "dump_*.py"]:
    for f in glob.glob(pattern):
        if f not in ("apply_fixes_10.py", "push_batch10.py"):
            os.remove(f)
            print(f"removed {f}")

for f in glob.glob("core/assets/*.bak_batch*"):
    os.remove(f)
    print(f"removed {f}")

run("git add -A")
run('git commit -m "batch10: wire retry logic in _ollama_stream, clean repo clutter"')
run("git push origin main")
print("Batch 10 pushed.")