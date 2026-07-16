import json
import os
from datetime import datetime


class MemoryEntry:

    def __init__(self, key, value, tags=None, source=None):
        self.key = key
        self.value = value
        self.tags = tags or []
        self.source = source or "runtime"
        self.created_at = datetime.now().isoformat()
        self.access_count = 0

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "tags": self.tags,
            "source": self.source,
            "created_at": self.created_at,
            "access_count": self.access_count,
        }


class RuntimeMemoryStore:
    """
    Persistent key-value memory store for Umbra.
    - Store facts, results, objectives, code snippets
    - Tag-based retrieval
    - Keyword search
    - Persist to disk between sessions
    - Eviction when store grows too large
    """

    def __init__(self, store_path=None, max_entries=1000):
        self.store_path = store_path or os.path.join(os.getcwd(), "sessions", "memory_store.json")
        self.max_entries = max_entries
        self.entries = {}
        self._load()

    def store(self, key, value, tags=None, source=None):
        entry = MemoryEntry(key, value, tags, source)
        self.entries[key] = entry
        if len(self.entries) > self.max_entries:
            self._evict_oldest()
        return entry

    def retrieve(self, key):
        entry = self.entries.get(key)
        if entry:
            entry.access_count += 1
        return entry

    def search(self, query, top_k=10):
        # Was pure substring containment ("games I like" not found in
        # "I like the games..." because word order differs) - use keyword
        # overlap instead so word order in the query doesn't matter, while
        # still rewarding an exact-phrase hit as a bonus.
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 1]
        results = []
        for entry in self.entries.values():
            value_lower = str(entry.value).lower()
            key_lower = entry.key.lower()
            tags_lower = [t.lower() for t in entry.tags]
            score = 0
            if query_lower in value_lower:
                score += 2
            if query_lower in key_lower:
                score += 3
            if any(query_lower in t for t in tags_lower):
                score += 1
            if query_words:
                value_hits = sum(1 for w in query_words if w in value_lower)
                key_hits = sum(1 for w in query_words if w in key_lower)
                score += value_hits
                score += key_hits * 2
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in results[:top_k]]

    def search_by_tag(self, tag):
        return [e for e in self.entries.values() if tag in e.tags]

    def delete(self, key):
        return self.entries.pop(key, None) is not None

    def clear(self):
        self.entries.clear()

    def list_keys(self):
        return list(self.entries.keys())

    def size(self):
        return len(self.entries)

    def save(self):
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        data = {k: v.to_dict() for k, v in self.entries.items()}
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        if not os.path.exists(self.store_path):
            return
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, entry_dict in data.items():
                entry = MemoryEntry(
                    entry_dict["key"],
                    entry_dict["value"],
                    entry_dict.get("tags", []),
                    entry_dict.get("source", "runtime"),
                )
                entry.created_at = entry_dict.get("created_at", entry.created_at)
                entry.access_count = entry_dict.get("access_count", 0)
                self.entries[key] = entry
        except Exception:
            self.entries = {}

    def _evict_oldest(self):
        sorted_entries = sorted(
            self.entries.items(),
            key=lambda x: (x[1].access_count, x[1].created_at),
        )
        to_remove = len(self.entries) - self.max_entries
        for key, _ in sorted_entries[:to_remove]:
            del self.entries[key]

    def get_stats(self):
        return {
            "total_entries": len(self.entries),
            "max_entries": self.max_entries,
            "total_accesses": sum(e.access_count for e in self.entries.values()),
        }