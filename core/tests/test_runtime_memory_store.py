import pytest
import os
from core.runtime.runtime_memory_store import RuntimeMemoryStore, MemoryEntry


@pytest.fixture
def store(tmp_path):
    return RuntimeMemoryStore(
        store_path=str(tmp_path / "memory.json"),
        max_entries=100,
    )


def test_store_and_retrieve(store):
    store.store("key1", "hello world", tags=["test"])
    entry = store.retrieve("key1")
    assert entry is not None
    assert entry.value == "hello world"


def test_retrieve_missing_returns_none(store):
    assert store.retrieve("missing_key") is None


def test_search_finds_by_value(store):
    store.store("doc1", "the autonomous runtime system", tags=["ai"])
    results = store.search("autonomous")
    assert len(results) > 0
    assert results[0].key == "doc1"


def test_search_finds_by_key(store):
    store.store("umbra_config", "configuration data")
    results = store.search("umbra_config")
    assert any(r.key == "umbra_config" for r in results)


def test_search_by_tag(store):
    store.store("a", "value a", tags=["python", "code"])
    store.store("b", "value b", tags=["config"])
    results = store.search_by_tag("python")
    assert len(results) == 1
    assert results[0].key == "a"


def test_delete_entry(store):
    store.store("del_me", "temporary")
    result = store.delete("del_me")
    assert result is True
    assert store.retrieve("del_me") is None


def test_delete_nonexistent(store):
    assert store.delete("nothing") is False


def test_size(store):
    store.store("x", 1)
    store.store("y", 2)
    assert store.size() == 2


def test_clear(store):
    store.store("x", 1)
    store.store("y", 2)
    store.clear()
    assert store.size() == 0


def test_list_keys(store):
    store.store("alpha", "a")
    store.store("beta", "b")
    keys = store.list_keys()
    assert "alpha" in keys
    assert "beta" in keys


def test_access_count_increments(store):
    store.store("tracked", "value")
    store.retrieve("tracked")
    store.retrieve("tracked")
    entry = store.retrieve("tracked")
    assert entry.access_count >= 2


def test_persist_and_reload(tmp_path):
    path = str(tmp_path / "mem.json")
    s1 = RuntimeMemoryStore(store_path=path)
    s1.store("persist_key", "persist_value", tags=["saved"])
    s1.save()
    s2 = RuntimeMemoryStore(store_path=path)
    entry = s2.retrieve("persist_key")
    assert entry is not None
    assert entry.value == "persist_value"


def test_eviction_at_max(tmp_path):
    store = RuntimeMemoryStore(store_path=str(tmp_path / "m.json"), max_entries=5)
    for i in range(10):
        store.store(f"key_{i}", f"value_{i}")
    assert store.size() <= 5


def test_get_stats(store):
    store.store("a", 1)
    stats = store.get_stats()
    assert "total_entries" in stats
    assert stats["total_entries"] == 1


def test_entry_to_dict():
    entry = MemoryEntry("k", "v", ["tag1"], "test")
    d = entry.to_dict()
    assert d["key"] == "k"
    assert d["value"] == "v"
    assert "tag1" in d["tags"]