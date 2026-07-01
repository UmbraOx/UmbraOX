import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout)
    print(r.stderr)

run("git add -A")
run('git commit -m "batch25: PyAudio auto-install with pipwin fallback"')
run("git push origin main")
print("Batch 25 pushed.")