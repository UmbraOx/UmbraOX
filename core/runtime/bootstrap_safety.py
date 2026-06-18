"""
Prevents runtime import crashes during partial cleanup.
"""

def safe_import(module_name, fallback=None):
    try:
        return __import__(module_name, fromlist=["*"])
    except Exception:
        return fallback