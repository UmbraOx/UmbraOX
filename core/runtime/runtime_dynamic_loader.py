import importlib


class RuntimeDynamicLoader:
    def load(self, module_name):
        return importlib.import_module(module_name)