import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch52: proactively close Player.sta/regen/def_power/gain_xp, Enemy.gold_drop, new Projectile patch"')
run("git push origin main")
print("Batch 52 pushed.")