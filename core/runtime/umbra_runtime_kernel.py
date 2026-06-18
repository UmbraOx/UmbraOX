from core.runtime.runtime_kernel import RuntimeKernel

class UmbraRuntimeKernel:
    """
    High-level orchestration wrapper over RuntimeKernel
    """

    def __init__(self, base_path: str):
        self.kernel = RuntimeKernel(base_path)
        self.base_path = base_path

    # -------------------------
    # BOOTSTRAP SYSTEM
    # -------------------------
    def bootstrap(self, module_registry: dict):
        """
        Inject all runtime modules into kernel
        """
        for name, module in module_registry.items():
            self.kernel.register_module(name, module)

    # -------------------------
    # START SYSTEM
    # -------------------------
    def start_system(self):
        self.kernel.start()

    def stop_system(self):
        self.kernel.stop()

    # -------------------------
    # DIRECT ACCESS LAYER
    # -------------------------
    def execute(self, fn, *args, **kwargs):
        return self.kernel.safe_execute(fn, *args, **kwargs)

    def get_kernel(self):
        return self.kernel