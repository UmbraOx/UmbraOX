import subprocess, sys

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(1)

run("git add -A")
run('git commit -m "batch17: version bump v3.0.0 -> v3.1.0"')
run("git push origin main")
print("Batch 17 pushed.")