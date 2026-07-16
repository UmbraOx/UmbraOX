import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak58_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''def _maybe_tts(runtime, text):
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

NEW = '''def _tts_log(line):
    """Diagnostic trail that bypasses whatever might be swallowing
    _umbra_print output from a background thread - writes ground truth
    to disk every single time TTS is invoked, regardless of whether
    anything reaches the GUI console pane."""
    try:
        _log_path = os.path.join(_UMBRA_ROOT, "sessions", "tts_debug.log")
        os.makedirs(os.path.dirname(_log_path), exist_ok=True)
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + line + "\\n")
    except Exception:
        pass


def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    _tts_log("_maybe_tts called, enabled=True, text_len=" + str(len(text or "")))
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            _tts_log("using external tts_engine module")
            tts_mod.run(text)
            return
        if not _ensure_pyttsx3():
            _tts_log("_ensure_pyttsx3() returned False - pyttsx3 not available, aborting")
            return
        # In-process pyttsx3 (even with COM init + engine reuse) can still
        # silently produce no audio at all when runAndWait() is called from
        # a background thread (which is how the GUI invokes this) - SAPI5
        # needs a message loop a worker thread doesn't have, and this
        # failure mode raises no Python exception. Run each utterance in
        # a fully isolated subprocess instead.
        _clean_text = "".join(c for c in text[:500] if ord(c) < 128) or "no speakable text"
        _tts_script = (
            "import pyttsx3,sys\\n"
            "e=pyttsx3.init()\\n"
            "e.say(sys.argv[1])\\n"
            "e.runAndWait()\\n"
        )
        _tts_log("launching subprocess, ascii-clean text_len=" + str(len(_clean_text)))
        _r = subprocess.run(
            [sys.executable, "-c", _tts_script, _clean_text],
            capture_output=True, text=True, timeout=30
        )
        _tts_log("subprocess returncode=" + str(_r.returncode) +
                 " stdout=" + repr((_r.stdout or "")[-200:]) +
                 " stderr=" + repr((_r.stderr or "")[-300:]))
        if _r.returncode != 0:
            _umbra_print("  [TTS] Error: " + (_r.stderr or "unknown")[-300:] + "\\n")
    except Exception as _tts_ex:
        _tts_log("EXCEPTION: " + repr(_tts_ex))
        _umbra_print("  [TTS] Error: " + str(_tts_ex) + "\\n")'''

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

print("Fix applied: TTS now writes sessions/tts_debug.log on every call (batch58)")