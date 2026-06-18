import os
import urllib.request
import json
import re


_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _ask_llm(prompt, model="llama3"):
    try:
        data = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False
        }).encode()

        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode()).get("response", "")

    except Exception:
        return ""


def _strip(code):
    code = re.sub(r"^```python", "", code, flags=re.MULTILINE)
    code = re.sub(r"```$", "", code)
    return code.strip()


class RuntimeAgentManager:
    """
    Minimal stable agent system (sprite + mechanics baseline).
    """

    def __init__(self, llm_provider=None):
        self.llm = llm_provider
        self.output_dir = os.path.join(_ROOT, "workspaces", "agents")
        os.makedirs(self.output_dir, exist_ok=True)

    def _call(self, prompt):
        if self.llm and self.llm.is_configured():
            r = self.llm.complete(prompt)
            if r.success:
                return r.content
        return _ask_llm(prompt)

    def sprite_agent(self, description):
        prompt = (
            "Write pygame sprite classes using ONLY draw functions.\n"
            + description
        )
        return _strip(self._call(prompt))

    def mechanics_agent(self, description):
        prompt = (
            "Write pure Python game mechanics classes (no pygame).\n"
            + description
        )
        return _strip(self._call(prompt))