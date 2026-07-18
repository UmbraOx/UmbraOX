import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch61: wire _maybe_tts into the general-knowledge Q&A path - the actual 4th and final answer branch"')
run("git push origin main")
print("Batch 61 pushed.")