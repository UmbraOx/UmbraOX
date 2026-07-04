import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch43: smoke test exercises .draw() for enemies/npcs/buildings too"')
run("git push origin main")
print("Batch 43 pushed.")