import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch53: wrap check_quest_kill/complete_ready_quests call sites defensively"')
run("git push origin main")
print("Batch 53 pushed.")