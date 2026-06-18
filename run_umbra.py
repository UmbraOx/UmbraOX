import time

from core.runtime.runtime_kernel import RuntimeKernel
from core.agents.boss_agent import BossAgent
from core.runtime.umbra_runtime_spine import UmbraRuntimeSpine

from core.runtime.runtime_self_upgrade_engine import RuntimeSelfUpgradeEngine
from core.runtime.runtime_watchdog import RuntimeWatchdog

from core.runtime.umbra_patch_approval_ui import UmbraPatchApprovalUI
from core.runtime.umbra_evolution_replay_logger import UmbraEvolutionReplayLogger
from core.runtime.umbra_multi_agent_specialization import UmbraMultiAgentSpecialization

from core.runtime.umbra_production_lock import UmbraProductionLock


def main():

    kernel = RuntimeKernel()

    boss = BossAgent(base_path="C:\\Umbra", auto_mode=True)

    upgrader = RuntimeSelfUpgradeEngine(
        root_dir="C:\\Umbra",
        kernel=kernel
    )

    watchdog = RuntimeWatchdog(kernel=kernel)

    approval_ui = UmbraPatchApprovalUI()

    logger = UmbraEvolutionReplayLogger()

    router = UmbraMultiAgentSpecialization()

    spine = UmbraRuntimeSpine(
        kernel=kernel,
        boss_agent=boss,
        upgrade_engine=upgrader,
        watchdog=watchdog,
        approval_ui=approval_ui,
        logger=logger,
        multi_agent_router=router,
        interval=5
    )

    # 🔒 PRODUCTION LOCK ATTACHMENT
    lock = UmbraProductionLock(spine, logger=logger)
    spine.production_lock = lock

    spine.start()

    print("Umbra Production Runtime ONLINE (LOCKED MODE)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        spine.stop()
        print("Umbra shutdown complete")


if __name__ == "__main__":
    main()