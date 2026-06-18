import inspect


class ConstructorContracts:
    """
    Validates required constructor arguments for runtime objects.
    """

    def validate(self, cls, provided_args: dict):
        try:
            sig = inspect.signature(cls.__init__)
            required = [
                p.name
                for p in sig.parameters.values()
                if p.name != "self" and p.default == inspect._empty
            ]

            missing = [r for r in required if r not in provided_args]

            if missing:
                return False, missing

            return True, None

        except Exception as e:
            return False, str(e)