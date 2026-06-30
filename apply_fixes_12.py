import os, shutil, datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"_deleted_tests_backup_{ts}"
os.makedirs(backup_dir, exist_ok=True)

targets = [
    "core/tests/test_runtime_agents.py",
    "core/tests/test_runtime_autonomous_brain.py",
    "core/tests/test_runtime_autonomous_pipeline.py",
    "core/tests/test_runtime_bootstrap.py",
    "core/tests/test_runtime_conversation_engine.py",
    "core/tests/test_runtime_live_prompt_session.py",
    "core/tests/test_runtime_llm_orchestrator.py",
    "core/tests/test_runtime_prompt_runtime.py",
    "core/tests/test_runtime_scheduler.py",
    "core/tests/test_runtime_self_analyzer.py",
    "core/tests/test_runtime_task_continuation.py",
    "core/tests/test_runtime_task_executor.py",
    "core/tests/test_runtime_task_planner.py",
    "core/tests/test_runtime_task_queue.py",
    "core/tests/test_runtime_task_state_machine.py",
    "core/tests/test_runtime_task_tree.py",
    "test_b.py",
    "test_retry.py",
    "tests/test_runtime_smoke.py",
]

deleted, missing = [], []
for t in targets:
    if os.path.exists(t):
        dest = os.path.join(backup_dir, t.replace("/", "_").replace("\\", "_"))
        shutil.copy(t, dest)
        os.remove(t)
        deleted.append(t)
    else:
        missing.append(t)

print(f"Deleted {len(deleted)} files (backed up to {backup_dir}):")
for d in deleted:
    print(f"  - {d}")
if missing:
    print(f"Not found ({len(missing)}):")
    for m in missing:
        print(f"  - {m}")