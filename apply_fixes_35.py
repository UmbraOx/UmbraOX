import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak35_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    MAX_RETRIES = 3
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
    return ""'''

NEW = '''    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 15, 30]
    # `timeout` passed to urlopen() is only a PER-READLINE socket timeout,
    # not a total budget. A slow-but-technically-alive Ollama connection
    # (trickling one token every few minutes) would never trip that and
    # could hang indefinitely, even though the caller asked for e.g. a
    # 10-minute budget. Enforce real wall-clock elapsed time too.
    _wall_start = _time.time()

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        if _time.time() - _wall_start > timeout:
            last_error = "wall-clock timeout after " + str(int(_time.time() - _wall_start)) + "s"
            _umbra_print(f"  [STREAM ERROR] {last_error}")
            break
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        # Per-readline socket timeout should not itself exceed the
        # remaining wall-clock budget.
        _remaining = max(5, timeout - (_time.time() - _wall_start))
        parts = []
        try:
            with _ur.urlopen(req, timeout=_remaining) as resp:
                while True:
                    if _time.time() - _wall_start > timeout:
                        raise TimeoutError("wall-clock timeout after " +
                                            str(int(_time.time() - _wall_start)) + "s")
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

        if _time.time() - _wall_start > timeout:
            break
        if attempt < MAX_RETRIES:
            _time.sleep(RETRY_DELAYS[attempt])

    _umbra_print(f"  [STREAM FAILED] giving up after {MAX_RETRIES+1} attempts: {last_error}")
    return ""'''

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

print("Fix applied: _ollama_stream now enforces real wall-clock timeout, won't hang past it (batch35)")