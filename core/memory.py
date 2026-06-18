from database.memory_db import MemoryDB


class MemorySystem:

    def __init__(self):
        self.db = MemoryDB()

    def recall(self, key="global"):
        data = self.db.load()
        return data

    def store(self, item):
        self.db.append({
            "item": item
        })