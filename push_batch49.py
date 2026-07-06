import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch49: play-last refuses a known-failed build unless overridden"')
run("git push origin main")
print("Batch 49 pushed.")