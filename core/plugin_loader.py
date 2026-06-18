import importlib

def load_plugins():
    plugins = ["core.plugins.fs_plugin"]

    for p in plugins:
        module = importlib.import_module(p)
        if hasattr(module, "load"):
            module.load()
            print(f"[PLUGIN] Loaded: {p.split('.')[-1]}")