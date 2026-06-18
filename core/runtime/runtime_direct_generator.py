"""
RuntimeDirectGenerator — unified with Umbra pipeline contract.
"""

import os
import urllib.request
import urllib.error
import json
from datetime import datetime


class DirectGenerationResult:

    def __init__(self, success, content, file_path=None, error=None, run_id=None, workspace=None):
        self.success = success
        self.content = content
        self.file_path = file_path
        self.error = error
        self.run_id = run_id
        self.workspace = workspace
        self.generated_at = datetime.now().isoformat()
        self.lines = len(content.splitlines()) if content else 0

    def to_dict(self):
        return {
            "success": self.success,
            "file_path": self.file_path,
            "workspace": self.workspace,
            "lines": self.lines,
            "error": self.error,
            "run_id": self.run_id,
            "generated_at": self.generated_at,
        }


class RuntimeDirectGenerator:

    def __init__(
        self,
        ollama_url="http://localhost:11434",
        model="qwen2.5-coder:14b",
        workspaces_dir=None,
        timeout=600
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.model = model
        self.workspaces_dir = workspaces_dir or os.path.join(os.getcwd(), "workspaces")
        self.timeout = timeout
        self.history = []
        self._run_counter = 0

    def generate(self, prompt, filename="output.py", project_name=None, show_progress=True):

        self._run_counter += 1
        run_id = f"direct_{self._run_counter:04d}"

        # unified workspace rule (MATCHES PIPELINE NOW)
        if project_name:
            workspace_root = os.path.join(self.workspaces_dir, "projects", project_name, run_id)
        else:
            workspace_root = os.path.join(self.workspaces_dir, run_id)

        code_dir = os.path.join(workspace_root, "code")
        os.makedirs(code_dir, exist_ok=True)

        file_path = os.path.join(code_dir, filename)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.15,
                "num_predict": 8192,
            }
        }

        full_response = []
        char_count = 0

        try:
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            if show_progress:
                print("  [GENERATING] ", end="", flush=True)

            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                while True:
                    line = resp.readline()
                    if not line:
                        break

                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        token = chunk.get("response", "")
                        full_response.append(token)
                        char_count += len(token)

                        if show_progress and char_count % 200 == 0:
                            print(".", end="", flush=True)

                        if chunk.get("done"):
                            break

                    except json.JSONDecodeError:
                        continue

            if show_progress:
                print(f" {char_count} chars")

            raw = "".join(full_response).strip()
            code = self._extract_code(raw)

            if not code or len(code) < 30:
                return DirectGenerationResult(
                    False, raw,
                    error="Response too short",
                    run_id=run_id,
                    workspace=workspace_root
                ), run_id

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return DirectGenerationResult(
                True, code,
                file_path=file_path,
                run_id=run_id,
                workspace=workspace_root
            ), run_id

        except Exception as e:
            return DirectGenerationResult(
                False, "",
                error=str(e),
                run_id=run_id,
                workspace=workspace_root
            ), run_id

    def _extract_code(self, text):
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            return text[start:end].strip() if end > start else text

        if "```" in text:
            parts = text.split("```")
            for i in range(1, len(parts), 2):
                block = parts[i]
                lines = block.splitlines()
                if lines and lines[0].lower() in ("python", "py", ""):
                    return "\n".join(lines[1:] if lines[0] else lines).strip()

        return text.strip()

    def is_available(self):
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags")
            urllib.request.urlopen(req, timeout=3)
            return True
        except Exception:
            return False