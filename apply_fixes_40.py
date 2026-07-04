import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak40_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Enemy.__init__=_ne
except Exception: pass
\'\'\''''

NEW = '''                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Enemy.__init__=_ne
except Exception: pass
# UMBRA_METHOD_SAFETY_PATCH
# Constructor patches above only guarantee *attributes* exist. Agents also
# sometimes omit entire *methods* the skeleton calls unconditionally every
# frame (e.g. an NPC class with no .draw() at all) - each one of those was
# turning into its own one-off crash-and-patch cycle. Fix the whole class
# of bug at once: any contract class missing update()/draw() gets a safe
# no-op / simple fallback instead of crashing main()'s loop.
try:
    def _umbra_noop_method(self,*a,**kw):
        return None
    def _umbra_fallback_draw(self,surf,*a,**kw):
        try:
            _cx = a[0] if len(a)>0 else 0
            _cy = a[1] if len(a)>1 else 0
            _px = int(getattr(self,'x',0)) - int(_cx)
            _py = int(getattr(self,'y',0)) - int(_cy)
            pygame.draw.circle(surf,(200,180,120),(_px,_py),8)
        except Exception:
            pass
    for _cn in ('Player','Camera','Enemy','NPC','Projectile','FloatText','Building'):
        if _cn in dir():
            _cls = eval(_cn)
            if not hasattr(_cls,'update'):
                _cls.update = _umbra_noop_method
            if _cn in ('Enemy','NPC','Projectile','Building') and not hasattr(_cls,'draw'):
                _cls.draw = _umbra_fallback_draw
except Exception:
    pass
\'\'\''''

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

print("Fix applied: generic method-safety patch for all contract classes (batch40)")