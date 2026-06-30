import shutil, datetime, ast, sys, re

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch17_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    content = f.read()

count = content.count("v3.0.0")
content = content.replace("v3.0.0", "v3.1.0")

# Add a changelog entry near top docstring if "Fixes & Upgrades in v3.1.0:" header exists pattern
content = content.replace(
    "Fixes & Upgrades in v3.1.0:",
    "Fixes & Upgrades in v3.1.0:\n"
    "  - Fixed _ollama_stream retry loop (proper backoff, success-return)\n"
    "  - Added headless gameplay crash test (test_gameplay_crash.py)\n"
    "  - Cleaned up stale/orphaned test scaffolding\n",
    1
)

with open(UF, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Fix applied: bumped {count} occurrence(s) of v3.0.0 -> v3.1.0, added changelog entry")

with open(UF, "r", encoding="utf-8") as f:
    src = f.read()
try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)