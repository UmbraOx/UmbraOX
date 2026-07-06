import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch48: every entity draw() falls back safely on any runtime crash"')
run("git push origin main")
print("Batch 48 pushed.")