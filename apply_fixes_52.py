import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak52_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Player: add missing 'sta'/'max_sta' defaults (main() reads player.sta
#         every frame for the sprint mechanic - this was a ticking time bomb,
#         not yet crashed on, found by auditing main() rather than waiting) ---
OLD1 = '''                        ('x',400.0),('y',300.0),('cls',a[0] if a else 'Warrior')]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Player.__init__=_np
except Exception: pass'''

NEW1 = '''                        ('x',400.0),('y',300.0),('cls',a[0] if a else 'Warrior'),
                        ('sta',100.0),('max_sta',100.0)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
        # Same reasoning as attributes above: main() calls these three
        # methods on the player unconditionally every frame/kill. An
        # agent's Player without one of them used to be a guaranteed
        # crash the first time it was reached - give safe defaults.
        if not hasattr(self,'regen') or not callable(getattr(self,'regen',None)):
            self.regen = lambda dt: None
        if not hasattr(self,'def_power') or not callable(getattr(self,'def_power',None)):
            self.def_power = lambda: getattr(self,'defense',0)
        if not hasattr(self,'gain_xp') or not callable(getattr(self,'gain_xp',None)):
            def _umbra_gain_xp(amount):
                self.xp = getattr(self,'xp',0) + amount
            self.gain_xp = _umbra_gain_xp
    Player.__init__=_np
except Exception: pass'''

if OLD1 not in src:
    print("FAIL: Player patch anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: Player patch anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Enemy: add missing 'gold_drop' default (main() adds e.gold_drop to
#         player.gold on every kill - not yet crashed on, found by audit) ---
OLD2 = '''                        ('xp_val',edef.get('xp_val',15)),
                        ('spd',edef.get('spd',90)),
                        ('aggro',edef.get('aggro',200)),
                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:'''

NEW2 = '''                        ('xp_val',edef.get('xp_val',15)),
                        ('gold_drop',edef.get('gold_drop',edef.get('gold',5))),
                        ('spd',edef.get('spd',90)),
                        ('aggro',edef.get('aggro',200)),
                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:'''

if OLD2 not in src:
    print("FAIL: Enemy patch anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: Enemy patch anchor not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

# --- 3. New: Projectile attribute-default patch. Projectiles are usually
#         constructed inside agent (mechanic) code, not the skeleton, so
#         there's no single call site to add defaults at like Player/Enemy -
#         patch the constructor itself instead, wherever it's called from. ---
OLD3 = '''# UMBRA_METHOD_SAFETY_PATCH'''

NEW3 = '''# UMBRA_PROJECTILE_PATCH
# main() reads p.x, p.y, p.dmg, p.alive on every Projectile every frame.
# Unlike Player/Enemy, projectiles are usually constructed by the agent's
# own mechanic code rather than a fixed skeleton call site, so there's
# nowhere obvious to add defaults after construction - patch the
# constructor itself instead, so it's covered no matter where it's called.
try:
    if 'Projectile' in dir():
        _opr = Projectile.__init__
        def _nprj(self,*a,**kw):
            try:
                _opr(self,*a,**kw)
            except Exception:
                pass
            for _at,_dv in [('x',0.0),('y',0.0),('dmg',5),('alive',True)]:
                if not hasattr(self,_at): setattr(self,_at,_dv)
        Projectile.__init__ = _nprj
except Exception:
    pass
# UMBRA_METHOD_SAFETY_PATCH'''

if OLD3 not in src:
    print("FAIL: Projectile patch insertion anchor not found")
    sys.exit(1)
if src.count(OLD3) != 1:
    print("FAIL: Projectile patch insertion anchor not unique")
    sys.exit(1)
src = src.replace(OLD3, NEW3, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: proactively closed Player.sta/regen/def_power/gain_xp, Enemy.gold_drop, new Projectile patch (batch52)")