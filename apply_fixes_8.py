import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch8_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 0-indexed: line 725 (with) through line 743 (continue) need +4 indent
start = 724  # line 725
end = 742    # line 743 inclusive

if lines[start].strip().startswith("with _ur.urlopen") and lines[end].strip() == "continue":
    for i in range(start, end + 1):
        if lines[i].strip() == "":
            continue
        lines[i] = "    " + lines[i]
    print(f"Fix applied: indented lines {start+1}-{end+1} by 4 spaces")
else:
    print("FIX FAILED: unexpected content at target lines")
    print(repr(lines[start]))
    print(repr(lines[end]))
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