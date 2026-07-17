import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak60_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. Log unconditionally at the very top of _maybe_tts, before the
#         enabled-check, so we can see every call attempt regardless of
#         whether the function returns early ---
OLD1 = '''def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    _tts_log("_maybe_tts called, enabled=True, text_len=" + str(len(text or "")))'''

NEW1 = '''def _maybe_tts(runtime, text):
    _tts_log("_maybe_tts ENTRY, runtime_id=" + str(id(runtime)) +
             " _tts_enabled=" + repr(runtime.get("_tts_enabled")) +
             " text_len=" + str(len(text or "")))
    if not runtime.get("_tts_enabled"):
        _tts_log("_maybe_tts returning early - not enabled")
        return'''

if OLD1 not in src:
    print("FAIL: _maybe_tts entry anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: _maybe_tts entry anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Log at the tts on/off toggle itself, so we can see the exact
#         runtime object id being written to, and compare against the
#         id _maybe_tts reads from ---
OLD2 = '''    if cmd in ("tts on", "text to speech on", "speak responses",
               "turn on tts", "turn tts on", "enable tts"):
        runtime["_tts_enabled"] = True
        _umbra_print("  [TTS] Text-to-speech ON.\\n")
        return

    if cmd in ("tts off", "text to speech off", "stop speaking",
               "turn off tts", "turn tts off", "disable tts"):
        runtime["_tts_enabled"] = False
        _umbra_print("  [TTS] Text-to-speech OFF.\\n")
        return'''

NEW2 = '''    if cmd in ("tts on", "text to speech on", "speak responses",
               "turn on tts", "turn tts on", "enable tts"):
        runtime["_tts_enabled"] = True
        _tts_log("TOGGLE: tts on, runtime_id=" + str(id(runtime)))
        _umbra_print("  [TTS] Text-to-speech ON.\\n")
        return

    if cmd in ("tts off", "text to speech off", "stop speaking",
               "turn off tts", "turn tts off", "disable tts"):
        runtime["_tts_enabled"] = False
        _tts_log("TOGGLE: tts off, runtime_id=" + str(id(runtime)))
        _umbra_print("  [TTS] Text-to-speech OFF.\\n")
        return'''

if OLD2 not in src:
    print("FAIL: toggle anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: toggle anchor not unique")
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

print("Fix applied: unconditional TTS diagnostic logging - will now show every call attempt and runtime object identity (batch60)")