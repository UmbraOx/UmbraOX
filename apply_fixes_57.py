import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak57_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

# --- 1. TTS via isolated subprocess instead of in-process pyttsx3 ---
OLD1 = '''def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            tts_mod.run(text)
            return
        if not _ensure_pyttsx3():
            return
        # pyttsx3's SAPI5 driver on Windows is backed by a COM object that
        # is NOT safe to re-create on every call from a background thread
        # (which is how the GUI invokes this) - that mismatch is the most
        # common reason "tts on" silently does nothing at all. Initialize
        # COM for this thread if pywin32 is available, and reuse a single
        # cached engine instance instead of creating a new one every call.
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except Exception:
            pass
        engine = runtime.get("_tts_pyttsx3_engine")
        if engine is None:
            import pyttsx3
            engine = pyttsx3.init()
            runtime["_tts_pyttsx3_engine"] = engine
        engine.say(text)
        engine.runAndWait()
    except Exception as _tts_ex:
        # Was a bare "except: pass" - meant "tts on" could fail completely
        # silently with zero feedback, which is exactly what was reported.
        _umbra_print("  [TTS] Error: " + str(_tts_ex) + "\\n")'''

NEW1 = '''def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            tts_mod.run(text)
            return
        if not _ensure_pyttsx3():
            return
        # In-process pyttsx3 (even with COM init + engine reuse) can still
        # silently produce no audio at all when runAndWait() is called from
        # a background thread (which is how the GUI invokes this) - SAPI5
        # needs a message loop a worker thread doesn't have, and this
        # failure mode raises no Python exception, so nothing was ever
        # printed either. Sidestep the whole class of threading/COM
        # apartment issues by running each utterance in a fully isolated
        # subprocess instead - slower per-call, but reliable.
        _tts_script = (
            "import pyttsx3,sys\\n"
            "e=pyttsx3.init()\\n"
            "e.say(sys.argv[1])\\n"
            "e.runAndWait()\\n"
        )
        _r = subprocess.run(
            [sys.executable, "-c", _tts_script, text[:500]],
            capture_output=True, text=True, timeout=30
        )
        if _r.returncode != 0:
            _umbra_print("  [TTS] Error: " + (_r.stderr or "unknown")[-300:] + "\\n")
    except Exception as _tts_ex:
        _umbra_print("  [TTS] Error: " + str(_tts_ex) + "\\n")'''

if OLD1 not in src:
    print("FAIL: TTS anchor not found")
    sys.exit(1)
if src.count(OLD1) != 1:
    print("FAIL: TTS anchor not unique")
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)

# --- 2. Tolerate "turn on tts" / "turn off tts" phrasing (e.g. via voice) ---
OLD2 = '''    if cmd in ("tts on", "text to speech on", "speak responses"):
        runtime["_tts_enabled"] = True
        _umbra_print("  [TTS] Text-to-speech ON.\\n")
        return

    if cmd in ("tts off", "text to speech off", "stop speaking"):
        runtime["_tts_enabled"] = False
        _umbra_print("  [TTS] Text-to-speech OFF.\\n")
        return'''

NEW2 = '''    if cmd in ("tts on", "text to speech on", "speak responses",
               "turn on tts", "turn tts on", "enable tts"):
        runtime["_tts_enabled"] = True
        _umbra_print("  [TTS] Text-to-speech ON.\\n")
        return

    if cmd in ("tts off", "text to speech off", "stop speaking",
               "turn off tts", "turn tts off", "disable tts"):
        runtime["_tts_enabled"] = False
        _umbra_print("  [TTS] Text-to-speech OFF.\\n")
        return'''

if OLD2 not in src:
    print("FAIL: tts on/off anchor not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: tts on/off anchor not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

# --- 3. Tolerate "workplace" typo for "list workspace files" ---
OLD3 = '''    if "list workspace" in cmd or "workspace files" in cmd:
        handle_files_browser(runtime, "workspace")
        return'''

NEW3 = '''    if ("list workspace" in cmd or "workspace files" in cmd
            or "list workplace" in cmd or "workplace files" in cmd):
        handle_files_browser(runtime, "workspace")
        return'''

if OLD3 not in src:
    print("FAIL: list-workspace anchor not found")
    sys.exit(1)
if src.count(OLD3) != 1:
    print("FAIL: list-workspace anchor not unique")
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

print("Fix applied: TTS via isolated subprocess, workplace typo tolerance, turn-on/off-tts phrasing (batch57)")