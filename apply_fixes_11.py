import shutil, datetime, re, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

targets = [
    ("test_umbra_full.py", "sys.exit(0 if not FAIL_ else 1)"),
    ("test_dev_assistant.py", "sys.exit(0 if FAIL == 0 else 1)"),
]

for fname, exit_line in targets:
    shutil.copy(fname, f"{fname}.bak_batch11_{ts}")
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    if exit_line not in content:
        print(f"SKIP {fname}: exit line not found verbatim, manual check needed")
        continue

    guarded = f'if __name__ == "__main__":\n    {exit_line}\n'
    content = content.replace(exit_line, guarded.rstrip("\n"), 1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fix applied: guarded sys.exit() in {fname} behind __main__ check")

import ast
for fname, _ in targets:
    with open(fname, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        ast.parse(src)
        print(f"{fname} AST OK")
    except SyntaxError as e:
        print(f"AST ERROR {fname} line {e.lineno} : {e.msg}")
        sys.exit(1)