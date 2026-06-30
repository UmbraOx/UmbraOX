import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch10_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    src = f.read()

OLD = '''    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 15, 30]

    for attempt in range(MAX_RETRIES + 1):
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        parts = []
        try:
            with _ur.urlopen(req, timeout=timeout) as resp:
                while True:
                    line = resp.readline()
                    if not line:
                        break
                    try:
                        chunk = _j.loads(line.decode("utf-8", errors="replace"))
                        tok = chunk.get("response", "")
                        if tok:
                            parts.append(tok)
                            if token_cb:
                                try:
                                    token_cb(tok)
                                except Exception:
                                    pass
                        if chunk.get("done", False):
                            break
                    except Exception:
                        continue
        except Exception as ex:
            _umbra_print("  [STREAM ERROR] " + str(ex))
            return ""
    return "".join(parts)
'''

NEW = '''    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 15, 30]

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        parts = []
        try:
            with _ur.urlopen(req, timeout=timeout) as resp:
                while True:
                    line = resp.readline()
                    if not line:
                        break
                    try:
                        chunk = _j.loads(line.decode("utf-8", errors="replace"))
                        tok = chunk.get("response", "")
                        if tok:
                            parts.append(tok)
                            if token_cb:
                                try:
                                    token_cb(tok)
                                except Exception:
                                    pass
                        if chunk.get("done", False):
                            break
                    except Exception:
                        continue

            result = "".join(parts)
            if result:
                return result

            last_error = "empty response"
        except Exception as ex:
            last_error = str(ex)
            _umbra_print(f"  [STREAM ERROR] attempt {attempt+1}/{MAX_RETRIES+1}: {last_error}")

        if attempt < MAX_RETRIES:
            _time.sleep(RETRY_DELAYS[attempt])

    _umbra_print(f"  [STREAM FAILED] giving up after {MAX_RETRIES+1} attempts: {last_error}")
    return ""
'''

if OLD not in src:
    print("FIX FAILED: exact OLD block not found")
    sys.exit(1)

src = src.replace(OLD, NEW, 1)

with open(UF, "w", encoding="utf-8") as f:
    f.write(src)

print("Fix applied: wired retry logic (success-return, retry-on-empty/exception with backoff)")

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)