import os, shutil, datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"_deleted_tests_backup_{ts}"
os.makedirs(backup_dir, exist_ok=True)

targets = [
    "core/tests/test_runtime_agent_factory.py",
    "core/tests/test_runtime_daemon.py",
    "core/tests/test_runtime_execution_graph.py",
    "core/tests/test_runtime_full_integration.py",
    "core/tests/test_runtime_handoff_generator.py",
    "core/tests/test_runtime_llm_provider.py",
    "core/tests/test_runtime_llm_provider_groq.py",
    "core/tests/test_runtime_patch_engine.py",
    "core/tests/test_runtime_pipeline_monitor.py",
    "core/tests/test_runtime_project_builder.py",
    "core/tests/test_runtime_queue.py",
    "core/tests/test_runtime_self_improvement_loop.py",
    "core/tests/test_runtime_workspace_manager.py",
    "core/tests/test_umbra_entry.py",
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

print(f"Deleted {len(deleted)} stale test files (backed up to {backup_dir}):")
for d in deleted:
    print(f"  - {d}")
if missing:
    print(f"Not found ({len(missing)}):")
    for m in missing:
        print(f"  - {m}")