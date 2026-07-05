import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch45: full README rewrite - current state, conventions, features, now/next/later roadmap"')
run("git push origin main")
print("Batch 45 pushed.")