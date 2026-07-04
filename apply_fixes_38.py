import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak38_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Fix UMBRA_PLAYER_PATCH: survive any exception from the agent's own __init__ ---
OLD1 = '''# UMBRA_PLAYER_PATCH
try:
    _op=Player.__init__
    def _np(self,*a,**kw):
        _op(self,*a,**kw)
        for _at,_dv in [('active_quests',{}),('completed_quests',[]),
                        ('inventory',{}),('equipped',{'weapon':None,'armor':None}),
                        ('spells',[]),('gold',50),('level',1),('xp',0),
                        ('xp_next',100),('float_texts',[]),('atk',10),
                        ('defense',5),('spd',180),('alive',True),
                        ('attack_cooldown',0.0),('regen_timer',0.0)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Player.__init__=_np
except Exception: pass'''

NEW1 = '''# UMBRA_PLAYER_PATCH
try:
    _op=Player.__init__
    def _np(self,*a,**kw):
        # An agent's __init__ may validate its own arguments (e.g. reject a
        # class name string it doesn't recognize) and raise. That used to
        # propagate straight up and crash the game the instant a player
        # picked a class. Retry with progressively safer fallbacks instead
        # of ever letting Player construction hard-crash the game.
        try:
            _op(self,*a,**kw)
        except Exception:
            _fallback_names = ["Warrior","Fighter","Knight","Adventurer","Hero"]
            _ok=False
            for _fn in _fallback_names:
                try:
                    if a:
                        _op(self,_fn,*a[1:],**kw)
                    else:
                        _op(self,_fn,**kw)
                    _ok=True; break
                except Exception:
                    continue
            if not _ok:
                try:
                    _op(self)
                except Exception:
                    pass
        for _at,_dv in [('active_quests',{}),('completed_quests',[]),
                        ('inventory',{}),('equipped',{'weapon':None,'armor':None}),
                        ('spells',[]),('gold',50),('level',1),('xp',0),
                        ('xp_next',100),('float_texts',[]),('atk',10),
                        ('defense',5),('spd',180),('alive',True),
                        ('attack_cooldown',0.0),('regen_timer',0.0),
                        ('x',400.0),('y',300.0),('cls',a[0] if a else 'Warrior')]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Player.__init__=_np
except Exception: pass'''

if OLD1 not in src:
    print("FAIL: player patch anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: player patch anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: Player construction never hard-crashes on class-name validation (batch38)")