import os
import subprocess
import urllib.request
import time


class RuntimeLauncher:
    """
    Service bootstrapper for Ollama + ComfyUI.
    """

    OLLAMA_URL = "http://localhost:11434"
    COMFYUI_URL = "http://localhost:8188"

    def __init__(self, auto_launch_comfyui=True):
        self.auto_launch_comfyui = auto_launch_comfyui

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

    def launch_comfyui(self):
        try:
            subprocess.Popen(["cmd", "/c", "start", "run_cpu.bat"], shell=True)
            time.sleep(5)
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