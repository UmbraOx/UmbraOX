import re, shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"

shutil.copy(UF, f"{UF}.bak_batch6_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Locate line 724 (1-indexed) "try:" that has no body before next def/blank-mismatch
idx = None
for i, l in enumerate(lines):
    if i + 1 == 724 and l.strip() == "try:":
        idx = i
        break

if idx is None:
    for i, l in enumerate(lines):
        if l.strip() == "try:" and (i + 1 >= len(lines) or lines[i + 1].strip() == ""):
            idx = i
            break

if idx is None:
    print("FIX FAILED: could not locate broken try block near line 724")
    sys.exit(1)

# Insert a safe stub body right after the bare try:
indent = len(lines[idx]) - len(lines[idx].lstrip())
stub = " " * (indent + 4) + "pass\n"
lines.insert(idx + 1, stub)

with open(UF, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Fix applied: inserted stub body after bare 'try:' at line {idx+1}")

with open(UF, "r", encoding="utf-8") as f:
    src = f.read()
try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)