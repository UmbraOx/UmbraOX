import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch27: wire listen/voice/tts commands into GUI command path"')
run("git push origin main")
print("Batch 27 pushed.")