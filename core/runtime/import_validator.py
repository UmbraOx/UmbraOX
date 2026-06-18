import importlib


class ImportValidator:
    """
    Ensures imports referenced in generated code actually exist.
    """

    def validate(self, module_name: str):
        try:
            importlib.import_module(module_name)
            return True, None
        except Exception as e:
            return False, str(e)