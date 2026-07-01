import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout)
    print(r.stderr)

run("git add -A")
run('git commit -m "batch22: background-thread gif/image generation, non-blocking GUI"')
run("git push origin main")
print("Batch 22 pushed.")