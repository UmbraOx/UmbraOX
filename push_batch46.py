import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch46: world-map safety patch (get_biome/get_tile never crash) + draw_world call-site net"')
run("git push origin main")
print("Batch 46 pushed.")