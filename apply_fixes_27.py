import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak27_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    if cmd in ("exit", "quit", "q"):
        _umbra_print("[UMBRA] Closing Umbra...")
        import os as _osexit; _osexit._exit(0)

    # Self-repair'''

NEW = '''    if cmd in ("exit", "quit", "q"):
        _umbra_print("[UMBRA] Closing Umbra...")
        import os as _osexit; _osexit._exit(0)

    # Voice / TTS (was interactive_mode-only; GUI now routes through here too)
    if cmd in ("voice on", "continuous voice on", "always listen"):
        runtime["_continuous_voice"] = True
        _umbra_print("  [MIC] Continuous voice ON.\\n")
        return

    if cmd in ("voice off", "continuous voice off", "stop listening"):
        runtime["_continuous_voice"] = False
        _umbra_print("  [MIC] Continuous voice OFF.\\n")
        return

    if cmd in ("tts on", "text to speech on", "speak responses"):
        runtime["_tts_enabled"] = True
        _umbra_print("  [TTS] Text-to-speech ON.\\n")
        return

    if cmd in ("tts off", "text to speech off", "stop speaking"):
        runtime["_tts_enabled"] = False
        _umbra_print("  [TTS] Text-to-speech OFF.\\n")
        return

    if cmd in ("listen", "voice", "speak", "mic"):
        v = runtime.get("voice_input")
        if not v or not v.is_available():
            _umbra_print("  Voice not available. pip install SpeechRecognition pyaudio\\n")
        else:
            _umbra_print("  [MIC] Listening...")
            res = v.listen_once(timeout=8, phrase_limit=20)
            if res.success and res.text.strip():
                _umbra_print("  [MIC] Heard: " + res.text)
                run_prompt(runtime, res.text)
            elif res.error:
                _umbra_print("  [MIC] Error: " + res.error + "\\n")
            else:
                _umbra_print("  [MIC] Nothing heard.\\n")
        return

    # Self-repair'''

if OLD not in src:
    print("FAIL: anchor block not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor block not unique")
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

print("Fix applied: listen/voice/tts commands now handled in GUI path (batch27)")