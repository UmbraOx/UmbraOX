import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak59_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    try:
        answer = _ollama_stream(
            _umbra_chat_prompt(prompt),
            timeout=120, num_predict=512, token_cb=_gui_cb)
        if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
            try: _gui_ref.stream_end()
            except Exception: pass
            print("")
        else:
            if answer:
                _umbra_print("\\n[UMBRA] " + answer.strip() + "\\n")
        return None'''

NEW = '''    try:
        answer = _ollama_stream(
            _umbra_chat_prompt(prompt),
            timeout=120, num_predict=512, token_cb=_gui_cb)
        if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
            try: _gui_ref.stream_end()
            except Exception: pass
            print("")
        else:
            if answer:
                _umbra_print("\\n[UMBRA] " + answer.strip() + "\\n")
        # This is the actual function generating plain Q&A answers in the
        # GUI (confirmed by the unique "[UMBRA] Thinking..." print above) -
        # it never called _maybe_tts at all, which is the real reason TTS
        # was never heard. Wiring it in here, not just the other answer
        # path, is the fix - not another audio-layer change.
        if answer:
            _maybe_tts(runtime, answer)
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

print("Fix applied: _direct_llm_answer now calls _maybe_tts - the actual missing wiring (batch59)")