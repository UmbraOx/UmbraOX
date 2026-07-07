import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch50: Player gets draw() safety net; agent-gen timeout 30min -> 1hr per attempt"')
run("git push origin main")
print("Batch 50 pushed.")