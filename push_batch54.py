import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch54: broaden gaming-mode detection + manual override, fix NPC construction crash"')
run("git push origin main")
print("Batch 54 pushed.")