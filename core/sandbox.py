import os
from core.config import SANDBOX_PATH

os.makedirs(SANDBOX_PATH, exist_ok=True)

def safe_path(path):

    full = os.path.abspath(
        os.path.join(SANDBOX_PATH, path)
    )

    sandbox = os.path.abspath(SANDBOX_PATH)

    if not full.startswith(sandbox):
        raise Exception("Sandbox violation")

    return full