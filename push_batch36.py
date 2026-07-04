import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch36: _umbra_flex is name/type-aware, fixes object-vs-coordinate mismatches"')
run("git push origin main")
print("Batch 36 pushed.")