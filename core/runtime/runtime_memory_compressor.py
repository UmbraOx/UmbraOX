from __future__ import annotations


class RuntimeMemoryCompressor:
    def compress(self, memory: list) -> dict:
        return {
            "compressed_items": len(memory),
            "memory": memory[:10],
        }