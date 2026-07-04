import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch44: bring UMBRA_HANDOFF.md current (was stale since batch21), add future-scope roadmap"')
run("git push origin main")
print("Batch 44 pushed.")