import subprocess, sys

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(1)

run("git add -A")
run('git commit -m "batch20: real AnimateDiff GIF generation, dreamshaper_8 default checkpoint"')
run("git push origin main")
print("Batch 20 pushed.")