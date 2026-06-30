from core.runtime.runtime_task_tree import (
    RuntimeTaskTree,
)


def test_runtime_task_tree():
    tree = RuntimeTaskTree()

    tree.add_task(
        "root",
        "child_task",
    )

    tasks = tree.get_tasks("root")

    assert "child_task" in tasks