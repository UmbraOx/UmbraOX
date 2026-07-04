import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak42_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''        fixed = _ollama_stream(fix_prompt, model=model, timeout=120, num_predict=4096)'''
NEW = '''        # This asks the model to regenerate an ENTIRE file (up to 4096
        # tokens) - comparable in size/cost to a full agent generation call,
        # which observably takes 3-20+ minutes on this hardware. 120s was
        # never realistic here and was guaranteed to fail, wasting time by
        # always falling back to the far more expensive full-regeneration
        # path instead. This is a repair call specifically, not a project-
        # wide budget - the overall build can still take hours.
        fixed = _ollama_stream(fix_prompt, model=model, timeout=600, num_predict=4096)'''

if OLD not in src:
    print("FAIL: anchor not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: syntax-repair call timeout 120s -> 600s, matches realistic generation time (batch42)")