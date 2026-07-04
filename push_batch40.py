import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch40: generic method-safety patch - fixes whole missing-update/draw crash class"')
run("git push origin main")
print("Batch 40 pushed.")