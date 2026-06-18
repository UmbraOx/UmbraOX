import pytest
from core.runtime.runtime_context_builder import RuntimeContextBuilder, RuntimeContext


def make_builder():
    return RuntimeContextBuilder()


def test_build_returns_context():
    builder = make_builder()
    ctx = builder.build("build a REST API")
    assert isinstance(ctx, RuntimeContext)
    assert ctx.objective == "build a REST API"


def test_context_has_system_prompt():
    builder = make_builder()
    ctx = builder.build("objective")
    assert len(ctx.system_prompt) > 0


def test_context_default_role():
    builder = make_builder()
    ctx = builder.build("objective")
    assert ctx.agent_role == "autonomous_executor"


def test_context_custom_role():
    builder = make_builder()
    ctx = builder.build("objective", agent_role="code_generator")
    assert ctx.agent_role == "code_generator"


def test_to_prompt_string_contains_objective():
    builder = make_builder()
    ctx = builder.build("create a game engine")
    prompt = ctx.to_prompt_string()
    assert "create a game engine" in prompt


def test_to_prompt_string_contains_role():
    builder = make_builder()
    ctx = builder.build("task", agent_role="validator")
    prompt = ctx.to_prompt_string()
    assert "validator" in prompt


def test_build_coder_context():
    builder = make_builder()
    ctx = builder.build_coder_context("fix the bug", existing_code="x = 1", error_output="NameError")
    assert ctx.agent_role == "code_generator"
    assert "current_code" in ctx.current_files
    assert "last_error" in ctx.metadata


def test_build_planner_context():
    builder = make_builder()
    ctx = builder.build_planner_context("plan deployment", known_tasks=["task_a", "task_b"])
    assert ctx.agent_role == "task_planner"
    assert len(ctx.task_history) == 2


def test_build_validator_context():
    builder = make_builder()
    ctx = builder.build_validator_context("validate output", test_output="77 passed")
    assert ctx.agent_role == "validator"
    assert "test_output_preview" in ctx.metadata


def test_extra_metadata_injected():
    builder = make_builder()
    ctx = builder.build("task", extra_metadata={"batch": "1", "priority": "high"})
    assert ctx.metadata["batch"] == "1"
    assert ctx.metadata["priority"] == "high"


def test_inject_files():
    builder = make_builder()
    ctx = builder.build("task")
    builder.inject_files(ctx, {"main.py": "print('hello')", "util.py": "pass"})
    assert "main.py" in ctx.current_files
    assert "util.py" in ctx.current_files


def test_set_custom_system_prompt():
    builder = make_builder()
    builder.set_system_prompt("Custom system instructions.")
    ctx = builder.build("task")
    assert ctx.system_prompt == "Custom system instructions."


def test_context_to_dict():
    builder = make_builder()
    ctx = builder.build("test objective")
    d = ctx.to_dict()
    assert "objective" in d
    assert "agent_role" in d
    assert "built_at" in d


def test_memory_bridge_integration():
    class FakeMemory:
        def retrieve(self, query):
            return ["remembered fact about " + query]

    builder = RuntimeContextBuilder(memory_bridge=FakeMemory())
    ctx = builder.build("deploy the API")
    assert len(ctx.memory_entries) > 0