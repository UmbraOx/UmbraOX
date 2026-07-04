import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

# Untrack (but keep on disk) everything now correctly excluded, that was
# previously committed by accident under the old .gitignore patterns.
run('git rm -r --cached --ignore-unmatch "*.bak[0-9]*"')
run('git rm -r --cached --ignore-unmatch "*.bak_batch*"')
run('git rm -r --cached --ignore-unmatch "workspaces/agent_builds"')
run('git rm -r --cached --ignore-unmatch "workspaces/projects"')
run('git rm -r --cached --ignore-unmatch "workspaces/images"')

# fix_game2.py has an actual syntax error (doesn't even parse) and is a
# dead one-off script superseded by batch29/31/32's systemic fixes.
run('git rm -f --ignore-unmatch fix_game2.py')

run("git add -A")
run('git commit -m "batch33: fix .gitignore, untrack accumulated backup/build-artifact clutter"')
run("git push origin main")
print("Batch 33 pushed.")