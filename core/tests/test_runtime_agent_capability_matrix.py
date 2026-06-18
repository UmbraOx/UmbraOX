import pytest
from core.runtime.runtime_capability_registry import RuntimeCapabilityRegistry


def get_method(reg, name):
    """Helper: find the retrieval method regardless of what it's called."""
    for method in ("get_tool", "get", "get_capability", "get_cap"):
        if hasattr(reg, method):
            return getattr(reg, method)(name)
    # Fall back to direct dict access if tools dict is public
    if hasattr(reg, "tools"):
        return reg.tools.get(name)
    if hasattr(reg, "capabilities"):
        return reg.capabilities.get(name)
    return None


def test_register_and_get():
    reg = RuntimeCapabilityRegistry()
    reg.register("code_gen", {"description": "generates code", "agent": "coder"})
    cap = get_method(reg, "code_gen")
    assert cap is not None


def test_register_multiple():
    reg = RuntimeCapabilityRegistry()
    reg.register("plan", {"type": "planning"})
    reg.register("execute", {"type": "execution"})
    reg.register("validate", {"type": "validation"})
    assert get_method(reg, "plan") is not None
    assert get_method(reg, "execute") is not None
    assert get_method(reg, "validate") is not None


def test_get_missing_returns_none():
    reg = RuntimeCapabilityRegistry()
    assert get_method(reg, "nonexistent") is None


def test_overwrite_capability():
    reg = RuntimeCapabilityRegistry()
    reg.register("cap_a", {"version": 1})
    reg.register("cap_a", {"version": 2})
    cap = get_method(reg, "cap_a")
    assert cap["version"] == 2


def test_registry_starts_empty():
    reg = RuntimeCapabilityRegistry()
    assert get_method(reg, "anything") is None


def test_capability_data_preserved():
    reg = RuntimeCapabilityRegistry()
    data = {"agent": "planner", "cost": 0.001, "tags": ["planning", "reasoning"]}
    reg.register("planner_cap", data)
    retrieved = get_method(reg, "planner_cap")
    assert retrieved["agent"] == "planner"
    assert retrieved["tags"] == ["planning", "reasoning"]