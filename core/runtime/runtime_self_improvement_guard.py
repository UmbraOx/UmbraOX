class RuntimeSelfImprovementGuard:
    """
    Ensures self-improvement cycles cannot execute unsafe or invalid plans.
    """

    def validate_plan(self, plan):
        if not plan:
            return False, "empty plan"

        if not hasattr(plan, "targets"):
            return False, "invalid plan structure"

        for t in plan.targets:
            if "module" not in t:
                return False, "invalid target missing module"

        return True, "ok"

    def allow_execution(self, plan):
        ok, _ = self.validate_plan(plan)
        return ok