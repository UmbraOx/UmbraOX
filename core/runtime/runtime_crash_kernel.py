import traceback


class RuntimeCrashKernel:
    """
    ISOLATED EXECUTION WRAPPER

    Prevents full system collapse from module failure
    """

    def __init__(self):
        self.errors = []

    def safe_call(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except Exception as e:
            self.errors.append({
                "error": str(e),
                "trace": traceback.format_exc()
            })

            return {
                "status": "failed_safe_isolation",
                "error": str(e)
            }