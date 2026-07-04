import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch37: automated headless smoke test after every build (catches crashes in seconds)"')
run("git push origin main")
print("Batch 37 pushed.")