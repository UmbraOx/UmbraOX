import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch30: strip stray top-level agent code (root cause of closes-on-launch bugs)"')
run("git push origin main")
print("Batch 30 pushed.")