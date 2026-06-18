import os
import sys

sys.path.append(os.getcwd())


def test_runtime_self_analyzer():
    from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer

    analyzer = RuntimeSelfAnalyzer()
    summary = analyzer.get_module_summary()

    print("[ANALYZER SUMMARY]", summary)

    assert isinstance(summary, dict)
    assert "total_modules" in summary


def test_runtime_memory_store():
    from core.runtime.runtime_memory_store import RuntimeMemoryStore

    store = RuntimeMemoryStore(max_entries=10)
    store.store("test_key", "hello world", tags=["test"])

    entry = store.retrieve("test_key")

    print("[MEMORY]", entry.to_dict())

    assert entry.value == "hello world"


def test_pipeline_execution():
    from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline

    pipeline = RuntimeExecutionPipeline()

    result = pipeline.run([
        {"task": "a"},
        {"task": "b"}
    ])

    print("[PIPELINE RESULT]", result)

    assert len(result) == 2


def test_improvement_loop_basic():
    from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer
    from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline
    from core.runtime.runtime_self_improvement_loop import RuntimeSelfImprovementLoop

    analyzer = RuntimeSelfAnalyzer()
    pipeline = RuntimeExecutionPipeline()

    loop = RuntimeSelfImprovementLoop(analyzer, pipeline)

    plan = loop.analyze_and_plan()

    print("[IMPROVEMENT PLAN]", plan.to_dict())

    assert plan is not None


if __name__ == "__main__":
    test_runtime_self_analyzer()
    test_runtime_memory_store()
    test_pipeline_execution()
    test_improvement_loop_basic()

    print("\nALL SMOKE TESTS PASSED")