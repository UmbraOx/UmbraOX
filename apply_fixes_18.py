import shutil, datetime, ast, sys, os

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# --- Fix 1: runtime_launcher.py ---
LF = "core/runtime/runtime_launcher.py"
shutil.copy(LF, f"{LF}.bak_batch18_{ts}")

new_launcher = '''import os
import subprocess
import urllib.request
import time


class RuntimeLauncher:
    """
    Service bootstrapper for Ollama + ComfyUI.
    """

    OLLAMA_URL = "http://localhost:11434"
    COMFYUI_URL = "http://localhost:8188"
    COMFYUI_DIR = r"C:\\ComfyUI"
    COMFYUI_LAUNCH_CANDIDATES = ["run_directml.bat", "run_amd.bat", "run_nvidia_gpu.bat", "run_cpu.bat"]

    def __init__(self, auto_launch_comfyui=True, comfyui_dir=None):
        self.auto_launch_comfyui = auto_launch_comfyui
        self.comfyui_dir = comfyui_dir or self.COMFYUI_DIR

    def check_ollama(self):
        try:
            urllib.request.urlopen(self.OLLAMA_URL, timeout=2)
            return True
        except Exception:
            return False

    def launch_ollama(self):
        if self.check_ollama():
            return True
        try:
            subprocess.Popen(["ollama", "serve"])
            time.sleep(3)
            return self.check_ollama()
        except Exception:
            return False

    def check_comfyui(self):
        try:
            urllib.request.urlopen(self.COMFYUI_URL, timeout=2)
            return True
        except Exception:
            return False

    def _find_comfyui_launch_script(self):
        if not os.path.isdir(self.comfyui_dir):
            return None
        for candidate in self.COMFYUI_LAUNCH_CANDIDATES:
            full = os.path.join(self.comfyui_dir, candidate)
            if os.path.exists(full):
                return full
        return None

    def launch_comfyui(self):
        script = self._find_comfyui_launch_script()
        if not script:
            return False
        try:
            subprocess.Popen(
                ["cmd", "/c", "start", "", os.path.basename(script)],
                cwd=self.comfyui_dir,
                shell=True,
            )
            # ComfyUI can take a while to load models on first start
            for _ in range(30):
                time.sleep(2)
                if self.check_comfyui():
                    return True
            return self.check_comfyui()
        except Exception:
            return False

    def ensure_services(self):
        status = {
            "ollama": self.check_ollama(),
            "comfyui": self.check_comfyui(),
        }

        if not status["ollama"]:
            status["ollama"] = self.launch_ollama()

        if not status["comfyui"] and self.auto_launch_comfyui:
            status["comfyui"] = self.launch_comfyui()

        return status
'''

with open(LF, "w", encoding="utf-8") as f:
    f.write(new_launcher)

print("Fix applied: runtime_launcher.py now targets C:\\ComfyUI and tries run_directml.bat first, with longer startup wait")

with open("pytest.ini", "r", encoding="utf-8") as f:
    ini = f.read()
if "test_gameplay_crash" not in ini:
    ini = ini.replace(
        "norecursedirs = sandbox _deleted_tests_backup_* venv .git __pycache__",
        "norecursedirs = sandbox _deleted_tests_backup_* venv .git __pycache__\ncollect_ignore = test_gameplay_crash.py"
    )
    with open("pytest.ini", "w", encoding="utf-8") as f:
        f.write(ini)
    print("pytest.ini updated to skip test_gameplay_crash.py (it's a manual script, not a pytest suite)")

# --- Fix 2: copy the corrected test_gameplay_crash.py (argv-safe) ---
gc_content = open("test_gameplay_crash.py", "r", encoding="utf-8").read()
if "_get_run_seconds" not in gc_content:
    print("WARNING: test_gameplay_crash.py still has the old unsafe argv parsing - will be fixed below")
    gc_content = gc_content.replace(
        'RUN_SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0',
        '''def _get_run_seconds():
    if len(sys.argv) > 1:
        try:
            return float(sys.argv[1])
        except ValueError:
            pass
    return 6.0


RUN_SECONDS = _get_run_seconds()'''
    )
    with open("test_gameplay_crash.py", "w", encoding="utf-8") as f:
        f.write(gc_content)
    print("Fix applied: test_gameplay_crash.py argv parsing made safe")
else:
    print("test_gameplay_crash.py already has safe argv parsing")

try:
    ast.parse(new_launcher)
    print(f"{LF} AST OK")
except SyntaxError as e:
    print(f"AST ERROR {LF} line {e.lineno} : {e.msg}")
    sys.exit(1)

try:
    ast.parse(gc_content)
    print("test_gameplay_crash.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR test_gameplay_crash.py line {e.lineno} : {e.msg}")
    sys.exit(1)