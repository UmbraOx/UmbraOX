from core.runtime.runtime_kernel import RuntimeKernel
from core.agents.boss_agent import BossAgent
from core.runtime.runtime_self_upgrade_engine import RuntimeSelfUpgradeEngine
from core.runtime.umbra_unified_runtime import UmbraUnifiedRuntime


def build_system(base_path="C:\\Umbra"):

    kernel = RuntimeKernel()

    boss = BossAgent(base_path=base_path, auto_mode=True)

    upgrade_engine = RuntimeSelfUpgradeEngine(
        root_dir=base_path,
        kernel=kernel
    )

    # placeholder watchdog (assumes exists elsewhere)
    watchdog = None

    runtime = UmbraUnifiedRuntime(
        kernel=kernel,
        boss_agent=boss,
        upgrade_engine=upgrade_engine,
        watchdog=watchdog,
        interval=5
    )

    return runtime


def start():
    system = build_system()
    system.start()
    return system


if __name__ == "__main__":
    start()