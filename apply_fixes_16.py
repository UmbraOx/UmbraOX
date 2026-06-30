content = '''"""
test_gameplay_crash.py -- Umbra gameplay crash test
Launches every built *_game.py under workspaces/agent_builds/, runs it
briefly in a subprocess with a dummy SDL video driver (headless), and
reports any crash / unhandled exception found in stderr.

Run: python test_gameplay_crash.py [seconds_per_game]
Exit code 0 if all games run clean, 1 if any crashed.
"""
import os
import sys
import glob
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILDS_DIR = os.path.join(ROOT, "workspaces", "agent_builds")
RUN_SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0

PY310_CANDIDATES = [
    r"C:\\Python310\\python.exe",
    os.path.join(os.path.expanduser("~"), "AppData", "Local", "Programs", "Python", "Python310", "python.exe"),
]
PYTHON_EXE = next((p for p in PY310_CANDIDATES if os.path.exists(p)), sys.executable)


def find_game_files():
    pattern = os.path.join(BUILDS_DIR, "*", "*_game.py")
    return sorted(glob.glob(pattern))


def run_game(path, seconds):
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"

    try:
        proc = subprocess.Popen(
            [PYTHON_EXE, path],
            cwd=os.path.dirname(path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
    except Exception as e:
        return True, "Failed to launch: " + str(e)

    try:
        out, err = proc.communicate(timeout=seconds)
        if proc.returncode not in (0, None) and err.strip():
            return True, "Exited code " + str(proc.returncode) + ":\\n" + err.strip()[-1500:]
        if "Traceback" in err:
            return True, "Traceback found despite clean exit:\\n" + err.strip()[-1500:]
        return False, "Exited cleanly (code " + str(proc.returncode) + ") before timeout"
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        if "Traceback" in err:
            return True, "Traceback found during run:\\n" + err.strip()[-1500:]
        return False, "Ran for full duration without crashing"


def main():
    games = find_game_files()
    if not games:
        print("[CRASH TEST] No *_game.py files found under " + BUILDS_DIR)
        return 0

    print("[CRASH TEST] Found " + str(len(games)) + " game(s). Running " + str(RUN_SECONDS) + "s each, headless.")
    print("[CRASH TEST] Using interpreter: " + PYTHON_EXE + "\\n")

    results = []
    for path in games:
        name = os.path.basename(os.path.dirname(path))
        print("  Testing: " + name + " (" + os.path.basename(path) + ") ...", end=" ", flush=True)
        t0 = time.time()
        crashed, detail = run_game(path, RUN_SECONDS)
        elapsed = time.time() - t0
        status = "CRASH" if crashed else "OK"
        print("[" + status + "] (" + ("%.1f" % elapsed) + "s)")
        if crashed:
            print("    " + detail + "\\n")
        results.append((name, crashed, detail))

    crashed_count = sum(1 for _, c, _ in results if c)
    print("=" * 60)
    print("  GAMEPLAY CRASH TEST: " + str(len(results) - crashed_count) + "/" + str(len(results)) + " PASSED")
    print("=" * 60)
    if crashed_count:
        print("\\nCrashed games:")
        for name, crashed, detail in results:
            if crashed:
                print("  x " + name)
        return 1
    print("\\nAll games launched and ran without crashing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

with open("test_gameplay_crash.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Created test_gameplay_crash.py")

import ast
try:
    ast.parse(content)
    print("test_gameplay_crash.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR: line {e.lineno} : {e.msg}")
    import sys
    sys.exit(1)