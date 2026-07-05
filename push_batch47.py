import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch47: smoke test exercises draw_world across camera positions incl. edges"')
run("git push origin main")
print("Batch 47 pushed.")