import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak25_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    # Auto-install required packages if missing
    _boot_deps = [("PIL","Pillow"),("pygame","pygame"),("requests","requests"),
                  ("numpy","numpy"),("pyttsx3","pyttsx3"),("speech_recognition","SpeechRecognition")]
    for _pkg_import, _pkg_name in _boot_deps:
        try:
            __import__(_pkg_import)
        except ImportError:
            try:
                print("  [UMBRA] " + _pkg_name + " not found — installing automatically...")
                import subprocess as _sp2
                _r = _sp2.run([sys.executable, "-m", "pip", "install", _pkg_name, "--quiet"],
                              capture_output=True, text=True)
                if _r.returncode == 0:
                    print("  [UMBRA] " + _pkg_name + " installed OK.")
                else:
                    print("  [UMBRA] " + _pkg_name + " install failed: " + _r.stderr[:120])
            except Exception as _pe:
                print("  [UMBRA] Could not auto-install " + _pkg_name + ": " + str(_pe))
'''

NEW = '''    # Auto-install required packages if missing
    _boot_deps = [("PIL","Pillow"),("pygame","pygame"),("requests","requests"),
                  ("numpy","numpy"),("pyttsx3","pyttsx3"),("speech_recognition","SpeechRecognition")]
    for _pkg_import, _pkg_name in _boot_deps:
        try:
            __import__(_pkg_import)
        except ImportError:
            try:
                print("  [UMBRA] " + _pkg_name + " not found — installing automatically...")
                import subprocess as _sp2
                _r = _sp2.run([sys.executable, "-m", "pip", "install", _pkg_name, "--quiet"],
                              capture_output=True, text=True)
                if _r.returncode == 0:
                    print("  [UMBRA] " + _pkg_name + " installed OK.")
                else:
                    print("  [UMBRA] " + _pkg_name + " install failed: " + _r.stderr[:120])
            except Exception as _pe:
                print("  [UMBRA] Could not auto-install " + _pkg_name + ": " + str(_pe))

    # PyAudio: plain pip often lacks a Windows wheel match -> fallback to pipwin
    try:
        import pyaudio  # noqa
    except ImportError:
        import subprocess as _sp3
        print("  [UMBRA] PyAudio not found — installing automatically...")
        _r3 = _sp3.run([sys.executable, "-m", "pip", "install", "pyaudio", "--quiet"],
                        capture_output=True, text=True)
        _ok3 = _r3.returncode == 0
        if not _ok3:
            print("  [UMBRA] Direct PyAudio install failed — trying pipwin fallback...")
            _sp3.run([sys.executable, "-m", "pip", "install", "pipwin", "--quiet"],
                      capture_output=True, text=True)
            _r4 = _sp3.run([sys.executable, "-m", "pipwin", "install", "pyaudio"],
                            capture_output=True, text=True)
            _ok3 = _r4.returncode == 0
        try:
            import pyaudio  # noqa
            print("  [UMBRA] PyAudio installed OK." if _ok3 else "  [UMBRA] PyAudio import still failing after install attempts.")
        except ImportError:
            print("  [UMBRA] PyAudio install failed. Mic input unavailable — voice commands via text still work.")
'''

if OLD not in src:
    print("FAIL: boot_deps block not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: boot_deps block not unique")
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

print("Fix applied: PyAudio auto-install with pipwin fallback (batch25)")