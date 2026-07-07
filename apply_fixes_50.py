import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak50_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Add Player to the draw-fallback/safety-wrap list ---
OLD1 = '''            if _cn in ('Enemy','NPC','Projectile','Building'):
                if not hasattr(_cls,'draw'):
                    _cls.draw = _umbra_fallback_draw
                else:
                    _cls.draw = _umbra_make_safe_draw(_cls.draw, _umbra_fallback_draw)'''

NEW1 = '''            if _cn in ('Player','Enemy','NPC','Projectile','Building'):
                if not hasattr(_cls,'draw'):
                    _cls.draw = _umbra_fallback_draw
                else:
                    _cls.draw = _umbra_make_safe_draw(_cls.draw, _umbra_fallback_draw)'''

if OLD1 not in src:
    print("FAIL: draw-fallback class list anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: draw-fallback class list anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Raise the default per-agent generation timeout ---
OLD2 = '''def _ollama_stream(prompt, model=None, timeout=1800, num_predict=-1, token_cb=None):'''
NEW2 = '''def _ollama_stream(prompt, model=None, timeout=3600, num_predict=-1, token_cb=None):'''

if OLD2 not in src:
    print("FAIL: default timeout anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: default timeout anchor not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: Player gets draw() safety net too; agent-generation timeout 30min->1hr per attempt (batch50)")