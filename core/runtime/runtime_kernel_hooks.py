class RuntimeKernelHooks:
    """
    CONNECTS EVOLUTION SYSTEM INTO KERNEL TICK LOOP
    """

    def __init__(self, kernel, evolver, governor):
        self.kernel = kernel
        self.evolver = evolver
        self.governor = governor

    # -------------------------
    # ATTACH HOOKS
    # -------------------------
    def attach(self):
        self.kernel.register_module("evolver", self.evolver)
        self.kernel.register_module("governor", self.governor)

    # -------------------------
    # EVOLUTION TICK
    # -------------------------
    def evolution_tick(self):
        report = self.evolver.run_cycle(limit=3)

        for item in report.get("results", []):
            file_path = item.get("file")

            if file_path and self.governor.allow_patch(file_path):
                # auto-apply only safe items
                if item.get("valid") and item.get("applied") is False:
                    self.evolver.patch_engine.apply_patch(
                        item["proposal"],
                        str(self.evolver.backup_dir)
                    )