import subprocess

def run(cmd):
    r = subprocess.run(cmd, cwd=r"C:\Umbra", capture_output=True, text=True, shell=True)
    print(r.stdout); print(r.stderr)

run("git add -A")
run('git commit -m "batch59: wire _maybe_tts into _direct_llm_answer - the actual answer function, fixes TTS never firing"')
run("git push origin main")
print("Batch 59 pushed.")