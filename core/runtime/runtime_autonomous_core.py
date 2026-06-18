class RuntimeAutonomousCore:
    """
    Lightweight autonomous execution loop.
    Coordinates workers, dispatcher, queue, and events.
    """

    def __init__(self, pool, dispatcher, cycles, expansion, queue, events, sync, messenger):
        self.pool = pool
        self.dispatcher = dispatcher
        self.cycles = cycles
        self.expansion = expansion
        self.queue = queue
        self.events = events
        self.sync = sync
        self.messenger = messenger

    def execute(self, objective):
        try:
            cycle_tasks = self.cycles.expand(objective)
            expanded = self.expansion.expand(cycle_tasks)

            for item in expanded:
                self.queue.push(item)

            workers = self.pool.workers()
            dispatched = self.dispatcher.dispatch(expanded, workers)

            self.events.emit("execution_completed", dispatched)

            messages = []
            for w in workers:
                messages.append(
                    self.messenger.send("core", w, "continue")
                )

            state = {
                "objective": objective,
                "queue_size": self.queue.size(),
                "workers": workers,
                "tasks": dispatched,
            }

            synced = self.sync.synchronize(state)

            return {
                "objective": objective,
                "expanded": expanded,
                "execution": dispatched,
                "messages": messages,
                "state": synced,
            }

        except Exception as e:
            return {
                "error": str(e),
                "objective": objective,
                "status": "failed"
            }