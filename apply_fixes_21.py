import shutil, datetime, ast, sys, subprocess

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

GF = "core/runtime/runtime_animated_gif_generator.py"
shutil.copy(GF, f"{GF}.bak21_{ts}")

with open(GF, "r", encoding="utf-8") as f:
    src = f.read()

src = src.replace(
    'frame_count=16, width=512, height=512, steps=20, cfg=7.0',
    'frame_count=8, width=384, height=384, steps=16, cfg=7.0'
)
src = src.replace('"context_length": 16,', '"context_length": self.frame_count,')
src = src.replace('"context_overlap": 4,', '"context_overlap": 2,')

with open(GF, "w", encoding="utf-8") as f:
    f.write(src)

print("Fix applied: AnimateDiff 8 frames/384px/16 steps (VRAM-safe)")

try:
    ast.parse(src)
    print(f"{GF} AST OK")
except SyntaxError as e:
    print(f"AST ERROR {GF}: {e}"); sys.exit(1)

NEW_HANDOFF = open("update_handoff.py").read().split('"""')[1]
with open("UMBRA_HANDOFF.md", "w", encoding="utf-8") as f:
    f.write(NEW_HANDOFF)
print("UMBRA_HANDOFF.md updated to v3.1.0")

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr); sys.exit(1)

run("git add -A")
run('git commit -m "batch21: AnimateDiff VRAM-safe params, UMBRA_HANDOFF.md v3.1.0"')
run("git push origin main")
print("Batch 21 pushed.")