import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch7_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    lines = f.readlines()

idx = None
for i, l in enumerate(lines):
    if i + 1 == 725 and l.strip() == "pass":
        idx = i
        break

if idx is None:
    print("FIX FAILED: stub 'pass' not found at line 725")
    sys.exit(1)

del lines[idx]

with open(UF, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Fix applied: removed stub 'pass' at line {idx+1}")

with open(UF, "r", encoding="utf-8") as f:
    src = f.read()
try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)