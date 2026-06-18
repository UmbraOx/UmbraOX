from core.runtime.runtime_priority_scheduler import RuntimePriorityScheduler


def test_runtime_priority_scheduler():

    scheduler = RuntimePriorityScheduler()

    scheduler.schedule(
        1,
        "critical_task"
    )

    task = scheduler.next_task()

    assert task[1] == "critical_task"