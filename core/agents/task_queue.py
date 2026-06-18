from collections import deque


class EvolutionQueue:
    """
    Holds pending system upgrades safely
    """

    def __init__(self):
        self.q = deque()

    def add(self, item):
        self.q.append(item)

    def pop(self):
        if self.q:
            return self.q.popleft()
        return None

    def size(self):
        return len(self.q)