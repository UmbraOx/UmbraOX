import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch34: remove orphaned scripts/folders with zero references (repo cleanup)"')
run("git push origin main")
print("Batch 34 pushed.")