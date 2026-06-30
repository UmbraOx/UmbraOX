import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------------------------------------------------------
# Fix 1: runtime_launcher.py - accept verbose kwarg, never swallow errors silently
# ---------------------------------------------------------------
LF = "core/runtime/runtime_launcher.py"
shutil.copy(LF, f"{LF}.bak_batch19_{ts}")

with open(LF, "r", encoding="utf-8") as f:
    launcher_src = f.read()

OLD_METHOD = '''    def ensure_services(self):
        status = {
            "ollama": self.check_ollama(),
            "comfyui": self.check_comfyui(),
        }

        if not status["ollama"]:
            status["ollama"] = self.launch_ollama()

        if not status["comfyui"] and self.auto_launch_comfyui:
            status["comfyui"] = self.launch_comfyui()

        return status'''

NEW_METHOD = '''    def ensure_services(self, verbose=False):
        status = {
            "ollama": self.check_ollama(),
            "comfyui": self.check_comfyui(),
        }
        if verbose:
            print("  [LAUNCHER] Ollama running: " + str(status["ollama"]))
            print("  [LAUNCHER] ComfyUI running: " + str(status["comfyui"]))

        if not status["ollama"]:
            if verbose:
                print("  [LAUNCHER] Starting Ollama...")
            status["ollama"] = self.launch_ollama()
            if verbose:
                print("  [LAUNCHER] Ollama started: " + str(status["ollama"]))

        if not status["comfyui"] and self.auto_launch_comfyui:
            script = self._find_comfyui_launch_script()
            if verbose:
                if script:
                    print("  [LAUNCHER] Starting ComfyUI via " + script + " (this can take 30-60s)...")
                else:
                    print("  [LAUNCHER] No ComfyUI launch script found in " + self.comfyui_dir)
            status["comfyui"] = self.launch_comfyui()
            if verbose:
                print("  [LAUNCHER] ComfyUI started: " + str(status["comfyui"]))

        return status'''

if OLD_METHOD not in launcher_src:
    print("FIX FAILED: ensure_services method not found verbatim in runtime_launcher.py")
    sys.exit(1)

launcher_src = launcher_src.replace(OLD_METHOD, NEW_METHOD, 1)

with open(LF, "w", encoding="utf-8") as f:
    f.write(launcher_src)

print("Fix applied: ensure_services() now accepts verbose= kwarg and prints launch diagnostics")

try:
    ast.parse(launcher_src)
    print(f"{LF} AST OK")
except SyntaxError as e:
    print(f"AST ERROR {LF} line {e.lineno} : {e.msg}")
    sys.exit(1)

# ---------------------------------------------------------------
# Fix 2: Umbra.py - make the startup launcher call NOT silently swallow errors,
# and report status clearly instead of bare except: pass
# ---------------------------------------------------------------
UF = "Umbra.py"
shutil.copy(UF, f"{UF}.bak_batch19_{ts}")

with open(UF, "r", encoding="utf-8") as f:
    umbra_src = f.read()

OLD_BLOCK = '''    try:
        from core.runtime.runtime_launcher import RuntimeLauncher
        launcher = RuntimeLauncher(auto_launch_comfyui=True)
        launcher.ensure_services(verbose=True)
        if hasattr(launcher, "_comfyui_proc") and launcher._comfyui_proc:
            _comfyui_proc = launcher._comfyui_proc
    except Exception:
        pass'''

NEW_BLOCK = '''    try:
        from core.runtime.runtime_launcher import RuntimeLauncher
        launcher = RuntimeLauncher(auto_launch_comfyui=True)
        launcher.ensure_services(verbose=True)
        if hasattr(launcher, "_comfyui_proc") and launcher._comfyui_proc:
            _comfyui_proc = launcher._comfyui_proc
    except Exception as _launch_err:
        print("  [LAUNCHER] Service auto-launch failed: " + str(_launch_err))'''

if OLD_BLOCK not in umbra_src:
    print("FIX FAILED: launcher call block not found verbatim in Umbra.py")
    sys.exit(1)

umbra_src = umbra_src.replace(OLD_BLOCK, NEW_BLOCK, 1)

# ---------------------------------------------------------------
# Fix 3: robust image command matching (regex instead of fixed phrase list)
# ---------------------------------------------------------------
OLD_IMG = '''    _img_words = ["make an image","make image","create an image","generate an image",
                  "make a picture","draw an image","make 1 image","make 2 image",
                  "make 3 image","make 4 image","make 5 image","make 6 image",
                  "make 7 image","make 8 image","make 9 image","make 10 image"]
    if any(kw in lower_direct for kw in _img_words) or re.search(r"make \\d+ image", lower_direct):'''

NEW_IMG = '''    _img_pattern = re.compile(
        r"\\b(make|create|generate|draw)\\b.{0,15}\\b(an?|\\d+)?\\s*(image|images|picture|pictures|art|artwork)\\b"
    )
    if _img_pattern.search(lower_direct):'''

if OLD_IMG not in umbra_src:
    print("FIX FAILED: image word matching block not found verbatim in Umbra.py")
    sys.exit(1)

umbra_src = umbra_src.replace(OLD_IMG, NEW_IMG, 1)

with open(UF, "w", encoding="utf-8") as f:
    f.write(umbra_src)

print("Fix applied: launcher failures now print instead of silently swallowed")
print("Fix applied: image command matching now uses robust regex (catches 'make a image of X', 'draw artwork', etc)")

try:
    ast.parse(umbra_src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print(f"AST ERROR Umbra.py line {e.lineno} : {e.msg}")
    sys.exit(1)