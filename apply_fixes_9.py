import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch9_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    lines = f.readlines()

start = 743  # line 744 'except'
end = 745    # line 746 'return ""'

if lines[start].strip().startswith("except Exception as ex"):
    for i in range(start, end + 1):
        if lines[i].strip() == "":
            continue
        lines[i] = "    " + lines[i]
    print(f"Fix applied: indented lines {start+1}-{end+1} by 4 spaces")
else:
    print("FIX FAILED: unexpected content")
    print(repr(lines[start]))
    sys.exit(1)

with open(UF, "w", encoding="utf-8") as f:
    f.writelines(lines)

with open(UF, "r", encoding="utf-8") as f:
    src = f.read()
try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)