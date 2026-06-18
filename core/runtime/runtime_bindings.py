def bind_systems(kernel, registry, upgrade_engine, watchdog):
    """
    CENTRALIZED WIRING FUNCTION

    Ensures:
    - single kernel authority
    - upgrade engine attached
    - watchdog monitoring active kernel
    - registry connected system-wide
    """

    kernel.attach_upgrade_engine(upgrade_engine)
    registry.register_kernel(kernel)

    if watchdog:
        watchdog.kernel = kernel

    return {
        "kernel": kernel,
        "registry": registry,
        "upgrade_engine": upgrade_engine,
        "watchdog": watchdog
    }