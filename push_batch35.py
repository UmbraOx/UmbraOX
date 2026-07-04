import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch35: enforce real wall-clock timeout in _ollama_stream (was hang-prone)"')
run("git push origin main")
print("Batch 35 pushed.")