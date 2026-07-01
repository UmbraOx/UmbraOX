import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout)
    print(r.stderr)

run("git add -A")
run('git commit -m "batch26: fix gif neon/flashing artifacts - cfg 8.5->7.0, color/flicker negatives"')
run("git push origin main")
print("Batch 26 pushed.")