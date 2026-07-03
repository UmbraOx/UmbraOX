import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch31: strip agent overrides of all UI contract functions - fixes shape-mismatch crashes"')
run("git push origin main")
print("Batch 31 pushed.")