import os
import sys
import traceback

sys.path.append(os.getcwd())


def banner(name):
    print("\n" + "=" * 60)
    print(f"[UMBRA TEST] {name}")
    print("=" * 60)


def test_runtime_self_analyzer():
    from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer

    banner("SELF ANALYZER")

    analyzer = RuntimeSelfAnalyzer()
    summary = analyzer.get_module_summary()

    print("[SUMMARY]", summary)

    assert isinstance(summary, dict)
    assert "total_modules" in summary


def test_runtime_memory_store():
    from core.runtime.runtime_memory_store import RuntimeMemoryStore

    banner("MEMORY STORE")

    store = RuntimeMemoryStore(max_entries=10)
    store.store("test_key", "hello world", tags=["test"])

    entry = store.retrieve("test_key")

    print("[ENTRY]", entry.to_dict())

    assert entry.value == "hello world"


def test_pipeline_execution():
    from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline

    banner("PIPELINE")

    pipeline = RuntimeExecutionPipeline()

    result = pipeline.run([
        {"task": "a"},
        {"task": "b"}
    ])

    print("[PIPELINE OBJECT]", result)
    print("[PIPELINE DICT]", result.to_dict())

    assert len(result) == 2


def test_improvement_loop_basic():
    from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer
    from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline
    from core.runtime.runtime_self_improvement_loop import RuntimeSelfImprovementLoop

    banner("IMPROVEMENT LOOP")

    analyzer = RuntimeSelfAnalyzer()
    pipeline = RuntimeExecutionPipeline()

    loop = RuntimeSelfImprovementLoop(analyzer, pipeline)

    plan = loop.analyze_and_plan()

    print("[PLAN]", plan.to_dict())

    assert plan is not None


def run_all():
    try:
        test_runtime_self_analyzer()
        test_runtime_memory_store()
        test_pipeline_execution()
        test_improvement_loop_basic()

        print("\n✅ ALL SMOKE TESTS PASSED")

    except Exception as e:
        print("\n❌ TEST FAILURE")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all()