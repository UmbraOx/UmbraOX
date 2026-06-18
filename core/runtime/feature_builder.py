from core.runtime.self_mod_engine import self_mod_engine
from core.runtime.system_introspector import system_introspector
from core.runtime.sandbox_runner import sandbox_runner
from core.runtime.safety_gate import safety_gate

class FeatureBuilder:

    def __init__(self):
        self.history = []

    def build_feature(self, path, new_code):
        """
        Full safe pipeline:
        propose → validate → sandbox → apply
        """

        # 1. safety check
        safe, reason = safety_gate.check(new_code)
        if not safe:
            return {"ok": False, "reason": reason}

        # 2. sandbox test
        test = sandbox_runner.run_python(new_code)

        if test["code"] != 0:
            return {
                "ok": False,
                "reason": "sandbox failed",
                "error": test
            }

        # 3. propose patch
        result = self_mod_engine.propose_change(path, new_code)

        if not result["ok"]:
            return result

        # 4. apply
        applied = self_mod_engine.apply_change(result["patch"])

        self.history.append(applied)

        return applied


feature_builder = FeatureBuilder()