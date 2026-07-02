import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak28_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Insert shared fallback-name helper ---
ANCHOR1 = '''# ============================================================
#  GAME CLARIFICATION QUESTIONS
# ============================================================

def _ask_game_clarifications(prompt, llm):'''

HELPER = '''# ============================================================
#  GAME NAME FALLBACK EXTRACTION
# ============================================================

_GAME_NAME_STOPWORDS = {
    "a","an","the","me","full","game","pygame","rpg","platformer","shooter",
    "puzzle","survival","strategy","horror","sci-fi","space","fighting",
    "clicker","roguelike","card","snake","racing","tower","dungeon",
    "version","test","small","of","my","like","with","called","named",
    "build","make","create","generate"
}

def _fallback_game_name(prompt):
    """Best-effort project name when no 'called X' / 'named X' phrase is present
    and no interactive stdin is available (e.g. GUI mode) to ask for one."""
    if not prompt:
        return None
    words = re.findall(r"[A-Za-z][A-Za-z0-9]*", prompt)
    verb_seen = False
    for w in words:
        lw = w.lower()
        if lw in ("build", "make", "create", "generate"):
            verb_seen = True
            continue
        if not verb_seen:
            continue
        if lw in _GAME_NAME_STOPWORDS:
            continue
        if len(w) < 3:
            continue
        return w[0].upper() + w[1:]
    return None


# ============================================================
#  GAME CLARIFICATION QUESTIONS
# ============================================================

def _ask_game_clarifications(prompt, llm):'''

if ANCHOR1 not in src:
    print("FAIL: helper anchor not found")
    sys.exit(1)
if src.count(ANCHOR1) != 1:
    print("FAIL: helper anchor not unique")
    sys.exit(1)
src = src.replace(ANCHOR1, HELPER, 1)

# --- 2. Deep-build site (interactive_mode, ~3839-3861) ---
OLD2 = '''                if not project_name:
                    try:
                        project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                    except (EOFError, KeyboardInterrupt):
                        project_name = "MyGame"'''
NEW2 = '''                if not project_name:
                    project_name = _fallback_game_name(raw) or _fallback_game_name(prompt)
                if not project_name:
                    try:
                        project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                    except (EOFError, KeyboardInterrupt):
                        project_name = "MyGame"'''

if OLD2 not in src:
    print("FAIL: deep-build site not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: deep-build site not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

# --- 3. Full-build site (_process_command GUI path, ~4244-4253) ---
OLD3 = '''            project_name = name_match.group(1).strip() if name_match else None
            if not project_name:
                try:
                    project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                except (EOFError, KeyboardInterrupt):
                    project_name = "MyGame"
            _umbra_print("\\n[UMBRA] Starting full deep build with all agents...")'''
NEW3 = '''            project_name = name_match.group(1).strip() if name_match else None
            if not project_name:
                project_name = _fallback_game_name(user_input)
            if not project_name:
                try:
                    project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                except (EOFError, KeyboardInterrupt):
                    project_name = "MyGame"
            _umbra_print("\\n[UMBRA] Starting full deep build with all agents...")'''

if OLD3 not in src:
    print("FAIL: full-build site not found")
    sys.exit(1)
if src.count(OLD3) != 1:
    print("FAIL: full-build site not unique")
    sys.exit(1)
src = src.replace(OLD3, NEW3, 1)

# --- 4. game_words branch _pname fallback (~3541) ---
OLD4 = '''        _pn_m = re.search(r"(?:called|named)\\s+([A-Za-z][A-Za-z0-9 ]+?)(?:[ ]|$|,|[.])", prompt, re.IGNORECASE)
        _pname = _pn_m.group(1).strip() if _pn_m else "MyGame"'''
NEW4 = '''        _pn_m = re.search(r"(?:called|named)\\s+([A-Za-z][A-Za-z0-9 ]+?)(?:[ ]|$|,|[.])", prompt, re.IGNORECASE)
        _pname = _pn_m.group(1).strip() if _pn_m else (_fallback_game_name(prompt) or "MyGame")'''

if OLD4 not in src:
    print("FAIL: game_words pname site not found")
    sys.exit(1)
if src.count(OLD4) != 1:
    print("FAIL: game_words pname site not unique")
    sys.exit(1)
src = src.replace(OLD4, NEW4, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: game name fallback extraction (no more silent MyGame in GUI) (batch28)")