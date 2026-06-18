from core.runtime.runtime_vector_memory import RuntimeVectorMemory


def test_runtime_vector_memory():

    memory = (
        RuntimeVectorMemory()
    )

    memory.store(
        "Umbra runtime execution"
    )

    results = memory.search(
        "runtime"
    )

    assert len(results) > 0