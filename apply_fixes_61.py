import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak61_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''            if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
                try: _gui_ref.stream_end()
                except Exception: pass
                print("")
            else:
                _umbra_print("\\n[UMBRA] " + (_ans.strip() if _ans else "I could not find an answer.") + "\\n")
        except Exception as _qe:
            _umbra_print("[UMBRA] Could not answer: " + str(_qe))
        return None'''

NEW = '''            if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
                try: _gui_ref.stream_end()
                except Exception: pass
                print("")
            else:
                _umbra_print("\\n[UMBRA] " + (_ans.strip() if _ans else "I could not find an answer.") + "\\n")
            # Found via exhaustive grep after _maybe_tts was already wired
            # into three OTHER answer paths and still never fired - this
            # general-knowledge Q&A branch (its own model selection, its
            # own streaming) was a genuinely separate, previously-missed
            # fourth path.
            if _ans:
                _maybe_tts(runtime, _ans)
        except Exception as _qe:
            _umbra_print("[UMBRA] Could not answer: " + str(_qe))
        return None'''

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

print("Fix applied: wired _maybe_tts into the general-knowledge Q&A path (_ans variable) (batch61)")