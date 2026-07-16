import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch56: wire 6 GUI-missing commands, fix silent TTS failure+threading, fix recall keyword matching"')
run("git push origin main")
print("Batch 56 pushed.")