class RuntimeLiveQueue:

    def __init__(self):

        self.queue = []

    def push(
        self,
        item
    ):

        self.queue.append(item)

    def pop(self):

        if not self.queue:
            return None

        return self.queue.pop(0)

    def size(self):

        return len(self.queue)