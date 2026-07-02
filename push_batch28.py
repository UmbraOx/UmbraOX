import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch28: fix game name extraction fallback (GUI no-stdin MyGame bug)"')
run("git push origin main")
print("Batch 28 pushed.")