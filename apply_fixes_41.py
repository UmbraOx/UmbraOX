import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak41_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    _game_words = ["make a game","build a game","create a game","generate a game",
                   "make me a game","build me a game","make a full game","build a full game",
                   "make an rpg","build an rpg","make a pygame","build a pygame",
                   "make a small","test version of","test game","make optiopia","build optiopia",
                   "make demiworld","build demiworld","make a platformer","make a shooter",
                   "make a dungeon","make a survival","make a version of my game",
                   "make a snake","build a snake","make snake","build snake",
                   "make a puzzle","build a puzzle","make a racing","build a racing",
                   "make a tower","build a tower","make a strategy","build a strategy",
                   "make a horror","build a horror","make a sci-fi","build a sci-fi",
                   "make a space","build a space","make a fighting","build a fighting",
                   "make a clicker","build a clicker","make a roguelike","build a roguelike",
                   "make overquest","build overquest","make a card","build a card"]
    if any(kw in lower_direct for kw in _game_words):'''

NEW = '''    # Was: a fixed list of exact phrases ("make a snake", "build a puzzle"...).
    # That missed anything with extra words in between, e.g. "make a 1 level
    # snake game" doesn't contain "make a snake" as a substring and fell
    # through to the generic (non-game-skeleton) pipeline entirely. Detect
    # intent instead: a build verb anywhere + a game-ish noun anywhere,
    # regardless of what's phrased in between.
    _build_verb_re = re.compile(r"\\b(make|build|create|generate)\\b", re.IGNORECASE)
    _game_noun_words = {
        "game","rpg","pygame","platformer","shooter","dungeon","survival",
        "snake","puzzle","racing","racer","tower","strategy","horror",
        "sci-fi","scifi","space","fighting","clicker","roguelike","card",
        "optiopia","demiworld","overquest",
    }
    _has_build_verb = bool(_build_verb_re.search(lower_direct))
    _has_game_noun = any(re.search(r"\\b" + re.escape(w) + r"\\b", lower_direct)
                          for w in _game_noun_words)
    if _has_build_verb and _has_game_noun:'''

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

print("Fix applied: game-detection now uses verb+noun co-occurrence instead of exact phrases (batch41)")