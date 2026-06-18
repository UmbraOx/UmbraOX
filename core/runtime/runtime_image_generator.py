import os
import json
import uuid
import urllib.request
from datetime import datetime


class ImageResult:
    def __init__(self, success, file_path=None, prompt=None, error=None, fallback_description=None):
        self.success = success
        self.file_path = file_path
        self.prompt = prompt
        self.error = error
        self.fallback_description = fallback_description
        self.generated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "success": self.success,
            "file_path": self.file_path,
            "prompt": self.prompt,
            "error": self.error,
            "fallback_description": self.fallback_description,
            "generated_at": self.generated_at,
        }


class RuntimeImageGenerator:
    """
    Robust ComfyUI image generator with:
    - structured prompt system
    - anatomy stabilization prompts
    - consistent sampler enforcement
    """

    COMFYUI_PORTS = [8188, 7861]

    # 🔥 LOCKED STABLE CONFIG
    DEFAULT_SAMPLER = "dpmpp_2m_sde"
    DEFAULT_STEPS = 28
    DEFAULT_CFG = 7.0
    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.path.join(os.getcwd(), "workspaces", "images")
        os.makedirs(self.output_dir, exist_ok=True)

        self._comfyui_url = "http://localhost:8188"
        self.history = []

    # -----------------------------
    # COMFYUI DETECTION
    # -----------------------------
    def is_available(self):
        for port in self.COMFYUI_PORTS:
            try:
                urllib.request.urlopen(f"http://localhost:{port}/system_stats", timeout=2)
                self._comfyui_url = f"http://localhost:{port}"
                return True
            except Exception:
                pass
        return False

    def _check_model_exists(self):
        model_path = r"C:\ComfyUI\models\checkpoints\dreamshaper_8.safetensors"
        return os.path.exists(model_path)

    # -----------------------------
    # PROMPT ENGINE (IMPORTANT)
    # -----------------------------
    def _build_prompt(self, prompt: str):
        """
        Forces anatomical correctness + realism stability
        """

        positive_prefix = (
            "highly detailed, ultra realistic, sharp focus, "
            "natural proportions, correct anatomy, symmetrical face, "
            "detailed eyes, clean structure, cinematic lighting, "
            "physically accurate body structure, professional rendering"
        )

        negative_prompt = (
            "worst quality, low quality, blurry, distorted, deformed, disfigured, "
            "bad anatomy, extra limbs, missing limbs, fused limbs, fused fingers, "
            "extra fingers, mutated hands, poorly drawn hands, poorly drawn feet, "
            "bad eyes, asymmetrical face, long neck, cropped, out of frame, "
            "artifact, watermark, text, noise, cross-eyed, lazy eye, asymmetrical eyes, "
            "deformed iris, deformed pupil, extra eye, mutated eyes, misaligned eyes, "
            "uneven eyes, bad anatomy, bad proportions, deformed face"
        )

        return positive_prefix + ", " + prompt, negative_prompt

    # -----------------------------
    # GENERATION
    # -----------------------------
    def generate(self, prompt, negative_prompt=None, width=None, height=None, steps=None, cfg=None, seed=None):

        if not self.is_available():
            result = ImageResult(
                success=False,
                prompt=prompt,
                error="ComfyUI not running",
                fallback_description="Start ComfyUI on port 8188"
            )
            self.history.append(result.to_dict())
            return result

        if not self._check_model_exists():
            result = ImageResult(
                success=False,
                prompt=prompt,
                error="Missing model checkpoint",
                fallback_description="Install dreamshaper_8.safetensors"
            )
            self.history.append(result.to_dict())
            return result

        width = width or self.DEFAULT_WIDTH
        height = height or self.DEFAULT_HEIGHT
        steps = steps or self.DEFAULT_STEPS
        cfg = cfg or self.DEFAULT_CFG

        actual_seed = seed if seed is not None else int(uuid.uuid4().int % (2**31))

        # 🔥 PROMPT ENGINE
        positive_prompt, auto_negative = self._build_prompt(prompt)
        negative_prompt = negative_prompt or auto_negative

        client_id = str(uuid.uuid4())

        workflow = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": self.DEFAULT_SAMPLER,
                    "scheduler": "normal",
                    "seed": actual_seed,
                    "steps": steps,
                    "latent_image": ["5", 0],
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": "dreamshaper_8.safetensors"}
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {"batch_size": 1, "height": height, "width": width}
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": positive_prompt}
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": negative_prompt}
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "umbra_image",
                    "images": ["8", 0]
                }
            },
        }

        try:
            payload = json.dumps({
                "prompt": workflow,
                "client_id": client_id
            }).encode("utf-8")

            req = urllib.request.Request(
                f"{self._comfyui_url}/prompt",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_data = json.loads(resp.read())

            prompt_id = resp_data.get("prompt_id", client_id)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            umbra_path = os.path.join(self.output_dir, f"image_{timestamp}.png")

            result = ImageResult(
                success=True,
                file_path=umbra_path,
                prompt=prompt,
            )

            result.prompt_id = prompt_id
            result.note = "Queued in ComfyUI"

            self.history.append(result.to_dict())
            return result

        except Exception as e:
            result = ImageResult(
                success=False,
                prompt=prompt,
                error=str(e),
                fallback_description="Generation failed"
            )
            self.history.append(result.to_dict())
            return result

    def get_history(self):
        return self.history