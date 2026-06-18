"""
Safe runtime import layer.

Prevents system-wide crashes from missing modules.
"""

def safe_import(module_path, fallback=None):
    try:
        return __import__(module_path, fromlist=["*"])
    except Exception:
        return fallback