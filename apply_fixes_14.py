import shutil, datetime, re, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
targets = ["test_umbra_full.py", "test_dev_assistant.py"]

for fname in targets:
    shutil.copy(fname, f"{fname}.bak_batch14_{ts}")
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # Rename function definition and all call sites: test( -> run_check(
    # Use word boundary to avoid touching test_* names
    new_content = re.sub(r'\bdef test\(', 'def run_check(', content)
    new_content = re.sub(r'(?<![\w.])test\(', 'run_check(', new_content)

    if new_content == content:
        print(f"SKIP {fname}: no changes made")
        continue

    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Fix applied: renamed test() helper to run_check() in {fname}")

with open("pytest.ini", "r", encoding="utf-8") as f:
    ini = f.read()
if "ignore = " not in ini:
    ini = ini.rstrip("\n") + "\nignore = test_umbra_full.py test_dev_assistant.py\n"
    with open("pytest.ini", "w", encoding="utf-8") as f:
        f.write(ini)
    print("Added ignore directives to pytest.ini for standalone test scripts")

import ast
for fname in targets:
    with open(fname, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        ast.parse(src)
        print(f"{fname} AST OK")
    except SyntaxError as e:
        print(f"AST ERROR {fname} line {e.lineno} : {e.msg}")
        sys.exit(1)