from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer
from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline
from core.runtime.runtime_self_improvement_loop import RuntimeSelfImprovementLoop
from core.runtime.runtime_daemon import RuntimeDaemon
from core.runtime.runtime_scheduler import RuntimeScheduler


class UmbraBootstrap:
    """
    Single entry point to start Umbra runtime system.
    """

    def __init__(self):
        self.analyzer = RuntimeSelfAnalyzer()
        self.pipeline = RuntimeExecutionPipeline()

        self.improvement = RuntimeSelfImprovementLoop(
            self.analyzer,
            self.pipeline,
        )

        self.daemon = RuntimeDaemon(self.improvement, interval_seconds=300)
        self.scheduler = RuntimeScheduler()

    def start(self):
        print("[UMBRA] Bootstrapping system...")

        self.scheduler.add_job(
            "self_improvement",
            self.improvement.run_cycle,
            300,
        )

        self.daemon.start()