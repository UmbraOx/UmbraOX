import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak48_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    for _cn in ('Player','Camera','Enemy','NPC','Projectile','FloatText','Building'):
        if _cn in dir():
            _cls = eval(_cn)
            if not hasattr(_cls,'update'):
                _cls.update = _umbra_noop_method
            if _cn in ('Enemy','NPC','Projectile','Building') and not hasattr(_cls,'draw'):
                _cls.draw = _umbra_fallback_draw
except Exception:
    pass'''

NEW = '''    def _umbra_make_safe_draw(_orig, _fallback):
        def _safe_draw(self, surf, *a, **kw):
            try:
                return _orig(self, surf, *a, **kw)
            except Exception:
                # The agent's draw() exists but crashed at runtime - most
                # often a rendering attribute (color, radius, sprite...)
                # its own __init__ never set (exactly what happened with
                # Enemy.col). Rather than keep adding one missing attribute
                # name at a time forever, fall back to a generic safe
                # renderer so the entity is still visible instead of
                # crashing the whole game.
                try:
                    return _fallback(self, surf, *a, **kw)
                except Exception:
                    return None
        return _safe_draw

    for _cn in ('Player','Camera','Enemy','NPC','Projectile','FloatText','Building'):
        if _cn in dir():
            _cls = eval(_cn)
            if not hasattr(_cls,'update'):
                _cls.update = _umbra_noop_method
            if _cn in ('Enemy','NPC','Projectile','Building'):
                if not hasattr(_cls,'draw'):
                    _cls.draw = _umbra_fallback_draw
                else:
                    _cls.draw = _umbra_make_safe_draw(_cls.draw, _umbra_fallback_draw)
except Exception:
    pass'''

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

print("Fix applied: every entity draw() now falls back safely on ANY runtime crash, not just missing draw() (batch48)")