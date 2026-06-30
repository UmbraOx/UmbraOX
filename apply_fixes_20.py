import shutil, datetime, ast, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
GF = "core/runtime/runtime_animated_gif_generator.py"
shutil.copy(GF, f"{GF}.bak_batch20_{ts}")

with open(GF, "r", encoding="utf-8") as f:
    gif_src = f.read()

OLD_HEADER = '''# C:\\Umbra\\core\\runtime\\runtime_animated_gif_generator.py
# Umbra Animated GIF Generator v2.0
# Uses PIL to create themed animations based on prompt keywords
import os, time, math, random, hashlib
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RuntimeAnimatedGifGenerator:
    def __init__(self, output_dir=None, **kwargs):
        self.output_dir = output_dir or os.path.join(_ROOT, "workspaces", "videos")
        os.makedirs(self.output_dir, exist_ok=True)
        self.ready = True
        try:
            from PIL import Image, ImageDraw
            self._pil = True
        except ImportError:
            self._pil = False; self.ready = False

    def is_available(self): return self.ready

    def run(self, prompt: str) -> dict:
        if not self.ready:
            return {"path": None, "error": "PIL not installed. pip install Pillow"}
        try:
            path = self._generate(prompt)
            return {"path": path, "error": None}'''

NEW_HEADER = '''# C:\\Umbra\\core\\runtime\\runtime_animated_gif_generator.py
# Umbra Animated GIF Generator v3.0
# Tries real ComfyUI + AnimateDiff-Evolved generation first (actual prompt-matched
# animation). Falls back to PIL procedural shapes only if ComfyUI/AnimateDiff
# is unavailable.
import os, time, math, random, hashlib
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_NEGATIVE_PROMPT = (
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, fused fingers, too many fingers, "
    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, flicker, "
    "inconsistent, poorly drawn hands, bad proportions, error, out of focus"
)
_QUALITY_SUFFIX = ", masterpiece, best quality, highly detailed, smooth animation, consistent character"


class RuntimeAnimatedGifGenerator:
    def __init__(self, output_dir=None, comfyui_url="http://127.0.0.1:8188",
                 checkpoint="dreamshaper_8.safetensors",
                 motion_module="mm_sd_v15_v2.ckpt",
                 frame_count=16, width=512, height=512, steps=20, cfg=7.0, **kwargs):
        self.output_dir = output_dir or os.path.join(_ROOT, "workspaces", "videos")
        os.makedirs(self.output_dir, exist_ok=True)
        self.comfyui_url = comfyui_url.rstrip("/")
        self.checkpoint = checkpoint
        self.motion_module = motion_module
        self.frame_count = frame_count
        self.width = width
        self.height = height
        self.steps = steps
        self.cfg = cfg
        self.ready = True
        self._comfy_ok = None
        try:
            from PIL import Image, ImageDraw
            self._pil = True
        except ImportError:
            self._pil = False; self.ready = False

    def is_available(self):
        return self.ready

    def _comfyui_available(self):
        if self._comfy_ok is not None:
            return self._comfy_ok
        try:
            import requests
            self._comfy_ok = requests.get(self.comfyui_url + "/system_stats", timeout=3).status_code == 200
        except Exception:
            self._comfy_ok = False
        return self._comfy_ok

    def run(self, prompt: str) -> dict:
        if self._comfyui_available():
            try:
                path = self._generate_animatediff(prompt)
                if path:
                    return {"path": path, "error": None}
            except Exception as e:
                # fall through to PIL fallback below
                self._last_comfy_error = str(e)
        if not self.ready:
            return {"path": None, "error": "ComfyUI unavailable and PIL not installed."}
        try:
            path = self._generate(prompt)
            return {"path": path, "error": None, "fallback": "ComfyUI/AnimateDiff unavailable - used PIL placeholder"}'''

if OLD_HEADER not in gif_src:
    print("FIX FAILED: header block not found verbatim in runtime_animated_gif_generator.py")
    sys.exit(1)

gif_src = gif_src.replace(OLD_HEADER, NEW_HEADER, 1)

# Insert the _generate_animatediff method right before the existing _generate method
ANCHOR = "    def _generate(self, prompt: str) -> str:"
ANIMATEDIFF_METHOD = '''    def _generate_animatediff(self, prompt: str) -> str:
        """Real animation via ComfyUI + AnimateDiff-Evolved. Returns output GIF path or raises."""
        import requests, json as _j, time as _time

        full_prompt = prompt + _QUALITY_SUFFIX
        seed = int(time.time()) % (2**31)

        workflow = {
            "1": {"class_type": "CheckpointLoaderSimple",
                  "inputs": {"ckpt_name": self.checkpoint}},
            "2": {"class_type": "ADE_AnimateDiffLoaderWithContext",
                  "inputs": {
                      "model": ["1", 0],
                      "model_name": self.motion_module,
                      "beta_schedule": "sqrt_linear (AnimateDiff)",
                      "context_options": ["3", 0],
                  }},
            "3": {"class_type": "ADE_AnimateDiffUniformContextOptions",
                  "inputs": {
                      "context_length": 16,
                      "context_stride": 1,
                      "context_overlap": 4,
                      "context_schedule": "uniform",
                      "closed_loop": False,
                      "fuse_method": "flat",
                  }},
            "4": {"class_type": "CLIPTextEncode",
                  "inputs": {"text": full_prompt, "clip": ["1", 1]}},
            "5": {"class_type": "CLIPTextEncode",
                  "inputs": {"text": _NEGATIVE_PROMPT, "clip": ["1", 1]}},
            "6": {"class_type": "EmptyLatentImage",
                  "inputs": {"width": self.width, "height": self.height, "batch_size": self.frame_count}},
            "7": {"class_type": "KSampler",
                  "inputs": {
                      "seed": seed, "steps": self.steps, "cfg": self.cfg,
                      "sampler_name": "euler_ancestral", "scheduler": "karras", "denoise": 1.0,
                      "model": ["2", 0], "positive": ["4", 0], "negative": ["5", 0],
                      "latent_image": ["6", 0],
                  }},
            "8": {"class_type": "VAEDecode",
                  "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
            "9": {"class_type": "ADE_AnimateDiffCombine",
                  "inputs": {
                      "images": ["8", 0],
                      "frame_rate": 8, "loop_count": 0,
                      "filename_prefix": "umbra_anim",
                      "format": "image/gif",
                      "pingpong": False, "save_image": True,
                  }},
        }

        r = requests.post(self.comfyui_url + "/prompt", json={"prompt": workflow}, timeout=15)
        if r.status_code != 200:
            raise RuntimeError("ComfyUI HTTP " + str(r.status_code) + ": " + r.text[:300])
        pid = r.json().get("prompt_id")
        if not pid:
            raise RuntimeError("No prompt_id returned")

        for _ in range(180):
            _time.sleep(2)
            hr = requests.get(self.comfyui_url + "/history/" + pid, timeout=5)
            if hr.status_code != 200:
                continue
            data = hr.json().get(pid, {})
            if not data.get("status", {}).get("completed"):
                continue
            for node_out in data.get("outputs", {}).values():
                for gif_info in node_out.get("gifs", []) + node_out.get("images", []):
                    fr = requests.get(
                        self.comfyui_url + "/view",
                        params={
                            "filename": gif_info["filename"],
                            "subfolder": gif_info.get("subfolder", ""),
                            "type": gif_info.get("type", "output"),
                        },
                        timeout=20,
                    )
                    if fr.status_code == 200:
                        ts_str = time.strftime("%Y%m%d_%H%M%S")
                        slug = prompt[:20].replace(" ", "_").replace("/", "")
                        out = os.path.join(self.output_dir, f"gif_{slug}_{ts_str}.gif")
                        with open(out, "wb") as f:
                            f.write(fr.content)
                        return out
            raise RuntimeError("Workflow completed but no gif/image output found")
        raise RuntimeError("Timeout waiting for AnimateDiff generation")

''' + ANCHOR

if ANCHOR not in gif_src:
    print("FIX FAILED: _generate anchor not found")
    sys.exit(1)

gif_src = gif_src.replace(ANCHOR, ANIMATEDIFF_METHOD, 1)

with open(GF, "w", encoding="utf-8") as f:
    f.write(gif_src)

print("Fix applied: RuntimeAnimatedGifGenerator now tries real ComfyUI+AnimateDiff-Evolved first, falls back to PIL only if unavailable")

try:
    ast.parse(gif_src)
    print(f"{GF} AST OK")
except SyntaxError as e:
    print(f"AST ERROR {GF} line {e.lineno} : {e.msg}")
    sys.exit(1)

# ---------------------------------------------------------------
# Fix 2: bump default image checkpoint to dreamshaper_8 (better anatomy/quality
# than base SD1.5), increase default steps for cleaner results
# ---------------------------------------------------------------
IF = "core/runtime/runtime_image_generator.py"
shutil.copy(IF, f"{IF}.bak_batch20_{ts}")

with open(IF, "r", encoding="utf-8") as f:
    img_src = f.read()

OLD_SIG = 'default_cfg=7.0,checkpoint="v1-5-pruned-emaonly.ckpt"):'
NEW_SIG = 'default_cfg=7.0,checkpoint="dreamshaper_8.safetensors"):'

if OLD_SIG not in img_src:
    print("FIX FAILED: image generator checkpoint default not found verbatim")
    sys.exit(1)

img_src = img_src.replace(OLD_SIG, NEW_SIG, 1)

OLD_STEPS = "default_steps=25,"
NEW_STEPS = "default_steps=30,"
if OLD_STEPS in img_src:
    img_src = img_src.replace(OLD_STEPS, NEW_STEPS, 1)

with open(IF, "w", encoding="utf-8") as f:
    f.write(img_src)

print("Fix applied: default image checkpoint -> dreamshaper_8.safetensors, steps 25 -> 30")

try:
    ast.parse(img_src)
    print(f"{IF} AST OK")
except SyntaxError as e:
    print(f"AST ERROR {IF} line {e.lineno} : {e.msg}")
    sys.exit(1)