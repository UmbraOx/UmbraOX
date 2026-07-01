import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout)
    print(r.stderr)

run("git add -A")
run('git commit -m "batch23: professional-grade image quality - negatives, dpmpp_2m, steps/cfg"')
run("git push origin main")
print("Batch 23 pushed.")