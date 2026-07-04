import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch42: syntax-repair call timeout 120s -> 600s"')
run("git push origin main")
print("Batch 42 pushed.")